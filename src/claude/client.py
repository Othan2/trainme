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
    
    def chat(self, message: str) -> str:
        """Simple chat interface with Claude."""
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            messages=[
                {"role": "user", "content": message}
            ]
        )
        return self._extract_text(response.content[0])
    
    def create_run_workout(self, workout_name: str, description: str = "") -> RunWorkout:
        """Create a structured RunWorkout with tool calling."""
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
                                "lower_bound": {"type": "number", "description": "Lower bound for cadence/pace ranges"},
                                "upper_bound": {"type": "number", "description": "Upper bound for cadence/pace ranges"}
                            },
                            "required": ["step_type", "duration_minutes", "target_type"]
                        }
                    }
                },
                "required": ["workout_name", "steps"]
            }
        }]
        
        prompt = f"""Create a running workout named '{workout_name}'. {description}

Please structure a workout with appropriate warmup, main workout sections, and cooldown. Use the create_workout tool to define each step.

For target types:
- no_target: Easy running
- heart_rate_zone: Use zone 1-5 (1=recovery, 2=aerobic, 3=tempo, 4=threshold, 5=VO2max)  
- cadence_range: Steps per minute (e.g., 160-180)
- pace_range: For pace zones, lower_bound should be SLOWER, upper_bound FASTER as it is measured in meters per second."""

        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1500,
            tools=tools,  # type: ignore
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Find the tool use in the response
        for content in response.content:
            if hasattr(content, 'type') and content.type == 'tool_use':
                return self._construct_run_workout(content.input)  # type: ignore
                
        # Fallback if no tool use found
        raise ValueError("Failed to create structured workout")
    
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
                    lower_bound=step_data["lower_bound"],
                    upper_bound=step_data["upper_bound"]
                )
            elif step_data["target_type"] == "pace_range":
                intensity = PaceZoneTarget(
                    lower_bound=step_data["lower_bound"],
                    upper_bound=step_data["upper_bound"]
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
