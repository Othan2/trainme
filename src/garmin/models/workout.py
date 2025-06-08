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


class IntensityTarget(ABC):
    @abstractmethod
    def to_target_dict(self) -> Dict[str, Any]:
        """Return the target type dictionary for API calls"""
        pass

@dataclass 
class NoTarget(IntensityTarget):
    target_value_unit: Optional[str] = None
    
    def to_target_dict(self) -> Dict[str, Any]:
        return {
            "workoutTargetTypeId": 1,
            "workoutTargetTypeKey": "no.target",
            "displayOrder": 1
        }

@dataclass
class CadenceTarget(IntensityTarget):
    # steps per minute
    lower_bound: float
    upper_bound: float
    target_value_unit: Optional[str] = None
    
    def __post_init__(self):
        if self.lower_bound >= self.upper_bound:
            raise ValueError(f"Lower bound ({self.lower_bound}) must be less than upper bound ({self.upper_bound})")
    
    def to_target_dict(self) -> Dict[str, Any]:
        return {
            "workoutTargetTypeId": 3,
            "workoutTargetTypeKey": "cadence", 
            "displayOrder": 3
        }

@dataclass
class HeartRateZoneTarget(IntensityTarget):
    # hr zone. could also do BPM range with bounds in future.
    zone_number: int
    target_value_unit: Optional[str] = None
    
    def to_target_dict(self) -> Dict[str, Any]:
        return {
            "workoutTargetTypeId": 4,
            "workoutTargetTypeKey": "heart.rate.zone",
            "displayOrder": 4
        }

@dataclass
class PaceZoneTarget(IntensityTarget):
    # TODO: figure out a better way to construct this - confusing that lower bound has to be higher than upper.
    lower_bound: float
    upper_bound: float
    target_value_unit: Optional[str] = None
    
    def __post_init__(self):
        if self.lower_bound < self.upper_bound:
            raise ValueError(f"Pace lower bound ({self.lower_bound}) must be greater than upper bound ({self.upper_bound}) - it is measured in meters per second")
    
    def to_target_dict(self) -> Dict[str, Any]:
        return {
            "workoutTargetTypeId": 6,
            "workoutTargetTypeKey": "pace.zone",
            "displayOrder": 6
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
    intensity: IntensityTarget
    
    def to_dict(self) -> Dict[str, Any]:
        result = {
            "stepOrder": self.step_order,
            "stepType": self.step_type.to_dict(),
            "type": "ExecutableStepDTO",
            "endCondition": self.end_condition.to_dict(),
            "endConditionValue": self.end_condition.value,
            "targetType": self.intensity.to_target_dict()
        }
        
        # Not sure if these ever need to be set...
        result["preferredEndConditionUnit"] = None
        result["endConditionCompare"] = None
        result["stepAudioNote"] = None
        
        # intensity
        if hasattr(self.intensity, 'lower_bound') and getattr(self.intensity, 'lower_bound', None) is not None:
            result["targetValueOne"] = getattr(self.intensity, 'lower_bound')
        if hasattr(self.intensity, 'upper_bound') and getattr(self.intensity, 'upper_bound', None) is not None:
            result["targetValueTwo"] = getattr(self.intensity, 'upper_bound')
        if hasattr(self.intensity, 'target_value_unit') and getattr(self.intensity, 'target_value_unit', None) is not None:
            result["targetValueUnit"] = getattr(self.intensity, 'target_value_unit')
        if hasattr(self.intensity, 'zone_number') and getattr(self.intensity, 'zone_number', None) is not None:
            result["zoneNumber"] = getattr(self.intensity, 'zone_number')
            
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
