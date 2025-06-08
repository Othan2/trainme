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
    
    def generate_workout(self, prompt: str) -> str:
        """Generate a workout based on the given prompt."""
        message = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return self._extract_text(message.content[0])
    
    def chat(self, message: str) -> tuple[str, RunWorkout | None]:
        """Chat interface with Claude that can also create workouts."""
        tools = [{
            "name": "create_workout",
            "description": "Create a structured running workout with warmup, intervals, and cooldown",
            "input_schema": {
                "type": "object",
                "properties": {
                    "workout_name": {"type": "string", "description": "Name of the workout"},
                    "steps": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "step_type": {
                                    "type": "string",
                                    "enum": ["warmup", "interval", "recovery", "cooldown", "rest", "other"],
                                    "description": "Type of workout step"
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
        }]
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            tools=tools,  # type: ignore
            messages=[
                {"role": "user", "content": message}
            ]
        )
        
        chat_response = ""
        workout = None
        
        for content in response.content:
            if hasattr(content, 'type') and content.type == 'text':
                chat_response = self._extract_text(content)
            elif hasattr(content, 'type') and content.type == 'tool_use':
                workout = self._construct_run_workout(content.input)  # type: ignore
                
        return chat_response, workout
    
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
