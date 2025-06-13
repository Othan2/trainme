from typing import Dict, Any
from .models.workout import (
    SportType,
    EndConditionType, 
    EndCondition,
    IntensityTarget,
    NoTarget,
    CadenceTarget,
    HeartRateZoneTarget,
    PaceZoneTarget,
    StepType,
    WorkoutStep,
    WorkoutSegment
)
from .models.run_workout import RunWorkout


class GarminWorkoutParser:
    """Parser to convert Garmin API workout JSON to RunWorkout objects"""
    
    @staticmethod
    def _parse_step_type(step_type_data: Dict[str, Any]) -> StepType:
        """Map JSON step type to StepType enum"""
        key = step_type_data.get("stepTypeKey")
        
        step_type_map = {
            "warmup": StepType.WARMUP,
            "cooldown": StepType.COOLDOWN, 
            "interval": StepType.INTERVAL,
            "recovery": StepType.RECOVERY,
            "rest": StepType.REST,
            "other": StepType.OTHER
        }
        
        return step_type_map[key or "other"]
    
    @staticmethod
    def _parse_end_condition(step_data: Dict[str, Any]) -> EndCondition:
        """Parse JSON end condition to EndCondition object"""
        end_condition_data = step_data.get("endCondition", {})
        condition_key = end_condition_data.get("conditionTypeKey")
        value = step_data.get("endConditionValue", 0.0)
        displayable = end_condition_data.get("displayable", True)
        
        condition_map = {
            "lap.button": EndConditionType.LAP_BUTTON,
            "time": EndConditionType.TIME,
            "distance": EndConditionType.DISTANCE,
            "calories": EndConditionType.CALORIES
        }
        
        condition_type = condition_map.get(condition_key, EndConditionType.LAP_BUTTON)
        return EndCondition(condition_type, value, displayable)
    
    @staticmethod
    def _parse_intensity_target(step_data: Dict[str, Any]) -> IntensityTarget:
        """Parse JSON target type to IntensityTarget object"""
        target_data = step_data.get("targetType", {})
        target_key = target_data.get("workoutTargetTypeKey")
        
        if target_key == "no.target":
            return NoTarget()
        elif target_key == "cadence":
            lower = step_data.get("targetValueOne")
            upper = step_data.get("targetValueTwo") 
            if lower is not None and upper is not None:
                return CadenceTarget(lower, upper)
            return NoTarget()
        elif target_key == "heart.rate.zone":
            zone = step_data.get("zoneNumber")
            if zone is not None:
                return HeartRateZoneTarget(zone)
            return NoTarget()
        elif target_key == "pace.zone":
            lower = step_data.get("targetValueOne")
            upper = step_data.get("targetValueTwo")
            if lower is not None and upper is not None:
                return PaceZoneTarget(lower, upper)
            return NoTarget()
        
        return NoTarget()
    
    @staticmethod
    def _parse_workout_step(step_data: Dict[str, Any]) -> WorkoutStep:
        """Parse JSON step data to WorkoutStep object"""
        step_order = step_data.get("stepOrder", 1)
        step_type = GarminWorkoutParser._parse_step_type(step_data.get("stepType", {}))
        end_condition = GarminWorkoutParser._parse_end_condition(step_data)
        intensity = GarminWorkoutParser._parse_intensity_target(step_data)
        
        return WorkoutStep(step_order, step_type, end_condition, intensity)
    
    @staticmethod
    def _parse_workout_segment(segment_data: Dict[str, Any]) -> WorkoutSegment:
        """Parse JSON segment data to WorkoutSegment object"""
        segment_order = segment_data.get("segmentOrder", 1)
        sport_type = SportType.RUNNING  # Assuming running for now
        
        workout_steps = []
        for step_data in segment_data.get("workoutSteps", []):
            if step_data.get("type") == "ExecutableStepDTO":
                workout_step = GarminWorkoutParser._parse_workout_step(step_data)
                workout_steps.append(workout_step)
        
        return WorkoutSegment(segment_order, sport_type, workout_steps)
    
    @staticmethod
    def parse_workout(workout_json: Dict[str, Any]) -> RunWorkout:
        """Parse complete JSON workout to RunWorkout object"""
        workout_name = workout_json.get("workoutName", "Untitled Workout")
        
        workout_segments = []
        for segment_data in workout_json.get("workoutSegments", []):
            segment = GarminWorkoutParser._parse_workout_segment(segment_data)
            workout_segments.append(segment)
        
        return RunWorkout(workout_name, workout_segments)