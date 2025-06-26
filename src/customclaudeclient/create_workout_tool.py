from typing import Dict, Any, List
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
    PaceZoneTarget,
)


CREATE_WORKOUTS_TOOL = {
    "name": "create_workouts",
    "description": """
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
                        "workout_name": {
                            "type": "string",
                            "description": "Name of the workout. Never include week information in the workout name, just a description of the workout.",
                        },
                        "steps": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "step_type": {
                                        "type": "string",
                                        "enum": [
                                            "warmup",
                                            "interval",
                                            "recovery",
                                            "cooldown",
                                            "rest",
                                        ],
                                        "description": "Type of workout step. Interval is the main work step.",
                                    },
                                    "duration_minutes": {
                                        "type": "number",
                                        "description": "Duration in minutes",
                                    },
                                    "target_type": {
                                        "type": "string",
                                        "enum": [
                                            "no_target",
                                            "heart_rate_zone",
                                            "cadence_range",
                                            "pace_range",
                                        ],
                                        "description": "Type of intensity target",
                                    },
                                    "zone_number": {
                                        "type": "integer",
                                        "description": "HR zone number (1-5) if target_type is heart_rate_zone",
                                    },
                                    "target_lower_bound": {
                                        "type": "number",
                                        "description": "Lower bound for cadence/pace ranges. For pace ranges, measured in MPH.",
                                    },
                                    "target_upper_bound": {
                                        "type": "number",
                                        "description": "Upper bound for cadence/pace ranges. For pace ranges, measured in MPH.",
                                    },
                                },
                                "required": [
                                    "step_type",
                                    "duration_minutes",
                                    "target_type",
                                ],
                            },
                        },
                    },
                    "required": ["workout_name", "steps"],
                },
            }
        },
        "required": ["workouts"],
    },
}


def _construct_run_workout(tool_output: Dict[str, Any]) -> RunWorkout:
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
                upper_bound=step_data["target_upper_bound"],
            )
        elif step_data["target_type"] == "pace_range":
            # Convert MPH to meters per second: MPH * 0.44704
            lower_bound_ms = step_data["target_lower_bound"] * 0.44704
            upper_bound_ms = step_data["target_upper_bound"] * 0.44704
            intensity = PaceZoneTarget(
                # invert bounds as pace range is in meters per second in garmin
                upper_bound=lower_bound_ms,
                lower_bound=upper_bound_ms,
            )
        else:
            intensity = NoTarget()

        # Create step
        step = WorkoutStep(
            step_order=i,
            step_type=StepType[step_data["step_type"].upper()],
            end_condition=EndCondition(
                condition_type=EndConditionType.TIME,
                value=step_data["duration_minutes"] * 60,  # Convert to seconds
            ),
            intensity=intensity,
        )
        workout_steps.append(step)

    # Create segment
    segment = WorkoutSegment(
        segment_order=1, sport_type=SportType.RUNNING, workout_steps=workout_steps
    )

    return RunWorkout(
        workout_name=tool_output["workout_name"], workout_segments=[segment]
    )


def handle_create_workouts_tool(
    tool_use, stored_workouts: Dict[str, RunWorkout]
) -> Dict[str, Any]:
    """Handle create_workouts tool execution."""
    # Extract workouts from tool_use
    current_use_workouts = []
    if (
        hasattr(tool_use, "input")
        and isinstance(tool_use.input, dict)
        and "workouts" in tool_use.input
    ):
        for workout_data in tool_use.input["workouts"]:  # type: ignore
            workout = _construct_run_workout(workout_data)
            current_use_workouts.append(workout)

    # Check for duplicate workout names
    duplicate_names = []
    valid_workouts = []

    for workout in current_use_workouts:
        if workout.workout_name in stored_workouts:
            duplicate_names.append(workout.workout_name)
        else:
            valid_workouts.append(workout)
            stored_workouts[workout.workout_name] = workout

    if duplicate_names:
        error_msg = f"Error: Workout names must be unique. The following names already exist: {', '.join(duplicate_names)}"
        return {
            "type": "tool_result",
            "tool_use_id": tool_use.id,
            "content": error_msg,
            "is_error": True,
            "workouts": [],
        }
    else:
        return {
            "type": "tool_result",
            "tool_use_id": tool_use.id,
            "content": str([str(w) + "\n" for w in valid_workouts]),
            "workouts": valid_workouts,
        }
