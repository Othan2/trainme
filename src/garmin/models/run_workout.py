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
    workout_name: str
    # Workout segments could be multiple types of activity, not just running. May want to allow that
    workout_segments: List[WorkoutSegment] = field(default_factory=list)
    is_wheelchair: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sportType": SportType(sport_type_id=1, sport_type_key="running", display_order=1).to_dict(),
            "subSportType": None,
            "workoutName": self.workout_name,
            "estimatedDistanceUnit": EstimatedDistanceUnit().to_dict(),
            "workoutSegments": [segment.to_dict() for segment in self.workout_segments],
            "avgTrainingSpeed": 0.0,
            # Left as zero in Garmin API request
            "estimatedDurationInSecs": 0,
            # Left as zero in Garmin API request
            "estimatedDistanceInMeters": 0,
            "estimateType": None,
            "isWheelchair": self.is_wheelchair
        }
