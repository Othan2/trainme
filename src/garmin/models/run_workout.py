from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
from .workout import (
    Workout,
    SportType, 
    WorkoutSegment, 
    EstimatedDistanceUnit,
    EndCondition,
    TargetType,
    WorkoutStep,
    StepType
)


@dataclass
class RunWorkout(Workout):
    sport_type: SportType
    workout_name: str
    # Workout segments could be multiple types of activity, not just running. May want to allow that
    workout_segments: List[WorkoutSegment] = field(default_factory=list)
    sub_sport_type: Optional[Any] = None
    estimated_distance_unit: EstimatedDistanceUnit = field(default_factory=EstimatedDistanceUnit)
    avg_training_speed: float = 0.0
    estimate_type: Optional[str] = None
    is_wheelchair: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sportType": self.sport_type.to_dict(),
            "subSportType": self.sub_sport_type,
            "workoutName": self.workout_name,
            "estimatedDistanceUnit": self.estimated_distance_unit.to_dict(),
            "workoutSegments": [segment.to_dict() for segment in self.workout_segments],
            "avgTrainingSpeed": self.avg_training_speed,
            # Left as zero in Garmin API request
            "estimatedDurationInSecs": 0,
            # Left as zero in Garmin API request
            "estimatedDistanceInMeters": 0,
            "estimateType": self.estimate_type,
            "isWheelchair": self.is_wheelchair
        }
