import anthropic
from anthropic.types import TextBlock
from typing import List, Dict, Any, cast
import json
from ..garmin.models.run_workout import RunWorkout
from ..garmin.models.workout import (
    WorkoutSegment, 
    WorkoutStep, 
    SportType,
    StepType,
    EndCondition,
    EndConditionType,
    NoTarget,
    CadenceTarget,
    HeartRateZoneTarget,
    PaceZoneTarget
)


class Claude:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.conversation_history = []
    
    def chat(self, message: str) -> tuple[str, List[RunWorkout] | None]:
        """Chat interface with Claude that can create workouts."""
        tools = [{
            "name": "create_workouts",
            "description": 
                """
                Create one or more structured running workouts with warmup, intervals, and cooldown.
                Workouts with higher intensities (e.g. zone 4 or 5 heart rate) should start with a 1 mile warmup and cooldown.
                Steady runs and long runs should be a single interval throughout.
                """,
            "input_schema": {
                "type": "object",
                "properties": {
                    "workouts": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "workout_name": {"type": "string", "description": "Name of the workout. Never include week information in the workout name, just a description of the workout."},
                                "steps": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "step_type": {
                                                "type": "string",
                                                "enum": ["warmup", "interval", "recovery", "cooldown", "rest"],
                                                "description": "Type of workout step. Interval is the main work step."
                                            },
                                            "duration_minutes": {"type": "number", "description": "Duration in minutes"},
                                            "target_type": {
                                                "type": "string", 
                                                "enum": ["no_target", "heart_rate_zone", "cadence_range", "pace_range"],
                                                "description": "Type of intensity target"
                                            },
                                            "zone_number": {"type": "integer", "description": "HR zone number (1-5) if target_type is heart_rate_zone"},
                                            "target_lower_bound": {"type": "number", "description": "Lower bound for cadence/pace ranges. For pace ranges, measured in MPH."},
                                            "target_upper_bound": {"type": "number", "description": "Upper bound for cadence/pace ranges. For pace ranges, measured in MPH."}
                                        },
                                        "required": ["step_type", "duration_minutes", "target_type"]
                                    }
                                }
                            },
                            "required": ["workout_name", "steps"]
                        }
                    }
                },
                "required": ["workouts"]
            }
        }]
        
        system_message = """
        Use the create_workouts tool to structure workouts rather than just describing them in text.
        You can create workouts in multiple responses if needed.
        If the user asks you to create a training plan, the user must specify number of runs per week and miles per week before you can use the create_workouts tool.
        
        You must run the following bits:
        - Any time the user responds with "yeah sure" or any variant of it, you must respond with: "Did you say "Yeah, sure" or "Yes sir"". You can vary this response a little if the user again responds with yeah sure.
        """
        
        # Add user message to history
        self.conversation_history.append({"role": "user", "content": message})
        
        chat_response = ""
        workouts = []
        
        while True:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=20000,
                system=system_message,
                tools=tools,  # type: ignore
                messages=self.conversation_history
            )
            
            print(f"Claude stop_reason: {response.stop_reason}")
            
            tool_uses = []
            
            current_use_workouts = []
            for content in response.content:
                if hasattr(content, 'type') and content.type == 'text':
                    text_content = self._extract_text(content)
                    chat_response += text_content
                elif hasattr(content, 'type') and content.type == 'tool_use':
                    tool_uses.append(content)
                    if hasattr(content, 'input') and isinstance(content.input, dict) and "workouts" in content.input:
                        for workout_data in content.input["workouts"]:  # type: ignore
                            current_use_workouts.append(self._construct_run_workout(workout_data))
            
            # Add Claude's response to history
            self.conversation_history.append({"role": "assistant", "content": response.content})
            
            # Add tool results if any tools were used
            if tool_uses:
                tool_results = []
                for tool_use in tool_uses:
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": tool_use.id,
                        "content": str([str(w) + "\n" for w in current_use_workouts])
                    })
                self.conversation_history.append({"role": "user", "content": tool_results})
            
            workouts.extend(current_use_workouts)
            
            # Continue if stop reason is tool_use, otherwise break.
            # Allows claude to generate a bunch of workouts at once.
            if response.stop_reason != "tool_use":
                break
                
        return chat_response, workouts
    
    def _construct_run_workout(self, tool_output: Dict[str, Any]) -> RunWorkout:
        """Convert tool input to RunWorkout object."""
        workout_steps = []
        
        for i, step_data in enumerate(tool_output["steps"], 1):
            # Create intensity target
            if step_data["target_type"] == "no_target":
                intensity = NoTarget()
            elif step_data["target_type"] == "heart_rate_zone":
                intensity = HeartRateZoneTarget(zone_number=step_data["zone_number"])
            elif step_data["target_type"] == "cadence_range":
                intensity = CadenceTarget(
                    lower_bound=step_data["target_lower_bound"],
                    upper_bound=step_data["target_upper_bound"]
                )
            elif step_data["target_type"] == "pace_range":
                # Convert MPH to meters per second: MPH * 0.44704
                lower_bound_ms = step_data["target_lower_bound"] * 0.44704
                upper_bound_ms = step_data["target_upper_bound"] * 0.44704
                intensity = PaceZoneTarget(
                    # invert bounds as pace range is in meters per second in garmin
                    upper_bound=lower_bound_ms,
                    lower_bound=upper_bound_ms
                )
            else:
                intensity = NoTarget()
            
            # Create step
            step = WorkoutStep(
                step_order=i,
                step_type=StepType[step_data["step_type"].upper()],
                end_condition=EndCondition(
                    condition_type=EndConditionType.TIME,
                    value=step_data["duration_minutes"] * 60  # Convert to seconds
                ),
                intensity=intensity
            )
            workout_steps.append(step)
        
        # Create segment
        segment = WorkoutSegment(
            segment_order=1,
            sport_type=SportType.RUNNING,
            workout_steps=workout_steps
        )
        
        return RunWorkout(
            workout_name=tool_output["workout_name"],
            workout_segments=[segment]
        )

    def _extract_text(self, content_block) -> str:
        """Extract text from content block."""
        if isinstance(content_block, TextBlock):
            return content_block.text
        return str(content_block)
    
    def _should_continue_conversation(self, response: str) -> bool:
        """Check if Claude's response indicates it wants to continue with more content."""
        continuation_indicators = [
            "I'll continue",
            "I'll finish", 
            "Let me continue",
            "I'll provide",
            "Next,",
            "Week 1:",  # Start of multi-week plan
            "continuing with",
            "moving on to",
            "Part 2",
            "Part 3",
        ]
        
        # Check for incomplete workout plans (mentions week 1 but not later weeks)
        if "Week 1" in response and "Week 2" not in response and "Week 3" not in response:
            return True
        
        # Check for continuation phrases
        response_lower = response.lower()
        return any(indicator.lower() in response_lower for indicator in continuation_indicators)
    
    def chat_complete(self, message: str) -> tuple[str, List[RunWorkout] | None]:
        """Chat with auto-continuation until Claude finishes the complete response."""
        all_workouts = []
        full_response = ""
        
        current_input = message
        while True:
            response, workouts = self.chat(current_input)
            full_response += response + " "
            
            if workouts:
                all_workouts.extend(workouts)
            
            if self._should_continue_conversation(response):
                current_input = "continue"
            else:
                break
        
        # Return summary of workouts created instead of garbled conversation
        if all_workouts:
            summary = f"Created {len(all_workouts)} workouts:\n"
            for i, workout in enumerate(all_workouts, 1):
                summary += f"{i}. {workout.workout_name}\n"
            return summary.strip(), all_workouts
        else:
            return full_response.strip(), None
