from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
from .workout import (
    WorkoutDetail,
    SportType, 
    WorkoutSegment, 
    EstimatedDistanceUnit,
)


@dataclass
class RunWorkout(WorkoutDetail):
    def __str__(self) -> str:
        segments_str = "\n".join(str(segment) for segment in self.workout_segments)
        return f"{self.workout_name}:\n{segments_str}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sportType": SportType.RUNNING.to_dict(),
            "subSportType": None,
            "workoutName": self.workout_name,
            "estimatedDistanceUnit": EstimatedDistanceUnit().to_dict(),
            "workoutSegments": [segment.to_dict() for segment in self.workout_segments],
            "avgTrainingSpeed": 0.0,
            "estimatedDurationInSecs": 0,
            "estimatedDistanceInMeters": 0,
            "estimateType": None,
            "isWheelchair": self.is_wheelchair
        }
