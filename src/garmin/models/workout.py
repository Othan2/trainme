from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from enum import Enum


class SportType(Enum):
    RUNNING = ("running", 1, 1)

    def to_dict(self) -> Dict[str, Any]:
        key, sport_id, display_order = self.value
        
        return {
            "sportTypeId": sport_id,
            "sportTypeKey": key,
            "displayOrder": display_order
        }


class EndConditionType(Enum):
    LAP_BUTTON = ("lap.button", 1, 1)
    TIME = ("time", 2, 2)
    DISTANCE = ("distance", 3, 3)
    CALORIES = ("calories", 4, 4)

    def to_dict(self) -> Dict[str, Any]:
        key, condition_id, display_order = self.value
        
        return {
            "conditionTypeId": condition_id,
            "conditionTypeKey": key,
            "displayOrder": display_order
        }


@dataclass
class EndCondition:
    condition_type: EndConditionType
    # Seconds for a time end condition. Meters for a distance or lap.button end condition.
    value: float
    displayable: bool = True

    def to_dict(self) -> Dict[str, Any]:
        condition_dict = self.condition_type.to_dict()
        condition_dict["displayable"] = self.displayable
        return condition_dict


class TargetType(Enum):
    NO_TARGET = ("no.target", 1, 1)
    CADENCE = ("cadence", 3, 3)
    HEART_RATE_ZONE = ("heart.rate.zone", 4, 4)
    PACE_ZONE = ("pace.zone", 6, 6)

    def to_dict(self) -> Dict[str, Any]:
        key, target_id, display_order = self.value
        
        return {
            "workoutTargetTypeId": target_id,
            "workoutTargetTypeKey": key,
            "displayOrder": display_order
        }


class StepType(Enum):
    WARMUP = ("warmup", 1, 1)
    COOLDOWN = ("cooldown", 2, 2)
    INTERVAL = ("interval", 3, 3)
    RECOVERY = ("recovery", 4, 4)
    REST = ("rest", 5, 5)
    OTHER = ("other", 7, 7)

    def to_dict(self) -> Dict[str, Any]:
        key, step_id, display_order = self.value
        
        return {
            "stepTypeId": step_id,
            "stepTypeKey": key,
            "displayOrder": display_order
        }


@dataclass
class WorkoutStep:
    step_order: int
    step_type: StepType
    end_condition: EndCondition
    target_type: TargetType
    type: str = "ExecutableStepDTO"
    preferred_end_condition_unit: Optional[str] = None
    end_condition_compare: Optional[str] = None
    target_value_one: Optional[float] = None
    target_value_two: Optional[float] = None
    target_value_unit: Optional[str] = None
    zone_number: Optional[int] = None
    step_audio_note: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "stepOrder": self.step_order,
            "stepType": self.step_type.to_dict(),
            "type": self.type,
            "endCondition": self.end_condition.to_dict(),
            "endConditionValue": self.end_condition.value,
            "targetType": self.target_type.to_dict()
        }
        
        # Only include non-default values
        if self.preferred_end_condition_unit is not None:
            result["preferredEndConditionUnit"] = self.preferred_end_condition_unit
        if self.end_condition_compare is not None:
            result["endConditionCompare"] = self.end_condition_compare
        if self.target_value_one is not None:
            result["targetValueOne"] = self.target_value_one
        if self.target_value_two is not None:
            result["targetValueTwo"] = self.target_value_two
        if self.target_value_unit is not None:
            result["targetValueUnit"] = self.target_value_unit
        if self.zone_number is not None:
            result["zoneNumber"] = self.zone_number
        if self.step_audio_note is not None:
            result["stepAudioNote"] = self.step_audio_note
            
        return result


@dataclass
class WorkoutSegment:
    segment_order: int
    sport_type: SportType
    workout_steps: List[WorkoutStep]

    def to_dict(self) -> Dict[str, Any]:
        workout_steps_dict = []
        for step in self.workout_steps:
            step_dict = step.to_dict()
            step_dict["stepId"] = step.step_order
            workout_steps_dict.append(step_dict)
        
        return {
            "segmentOrder": self.segment_order,
            "sportType": self.sport_type.to_dict(),
            "workoutSteps": workout_steps_dict
        }


@dataclass
class EstimatedDistanceUnit:
    unit_key: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {"unitKey": self.unit_key}


class Workout(ABC):
    """Base class for all workout types"""
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convert the workout to a dictionary representation for API calls"""
        pass
