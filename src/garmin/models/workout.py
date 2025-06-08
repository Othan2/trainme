from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
from abc import ABC, abstractmethod


@dataclass
class SportType:
    sport_type_id: int
    sport_type_key: str
    display_order: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sportTypeId": self.sport_type_id,
            "sportTypeKey": self.sport_type_key,
            "displayOrder": self.display_order
        }


@dataclass
class EndCondition:
    condition_type_id: int
    condition_type_key: str
    display_order: int
    displayable: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "conditionTypeId": self.condition_type_id,
            "conditionTypeKey": self.condition_type_key,
            "displayOrder": self.display_order,
            "displayable": self.displayable
        }


@dataclass
class TargetType:
    workout_target_type_id: int
    workout_target_type_key: str
    display_order: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "workoutTargetTypeId": self.workout_target_type_id,
            "workoutTargetTypeKey": self.workout_target_type_key,
            "displayOrder": self.display_order
        }


@dataclass
class StepType:
    step_type_id: int
    step_type_key: str
    display_order: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "stepTypeId": self.step_type_id,
            "stepTypeKey": self.step_type_key,
            "displayOrder": self.display_order
        }


@dataclass
class WorkoutStep:
    step_id: int
    step_order: int
    step_type: StepType
    end_condition: EndCondition
    target_type: TargetType
    type: str = "ExecutableStepDTO"
    end_condition_value: Optional[float] = None
    preferred_end_condition_unit: Optional[str] = None
    end_condition_compare: Optional[str] = None
    target_value_one: Optional[float] = None
    target_value_two: Optional[float] = None
    target_value_unit: Optional[str] = None
    zone_number: Optional[int] = None
    step_audio_note: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "stepId": self.step_id,
            "stepOrder": self.step_order,
            "stepType": self.step_type.to_dict(),
            "type": self.type,
            "endCondition": self.end_condition.to_dict(),
            "targetType": self.target_type.to_dict()
        }
        
        # Only include non-default values
        if self.end_condition_value is not None:
            result["endConditionValue"] = self.end_condition_value
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
    workout_steps: List[WorkoutStep] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "segmentOrder": self.segment_order,
            "sportType": self.sport_type.to_dict(),
            "workoutSteps": [step.to_dict() for step in self.workout_steps]
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


# Helper functions for common step types
def create_running_sport_type() -> SportType:
    return SportType(sport_type_id=1, sport_type_key="running", display_order=1)


def create_no_target() -> TargetType:
    return TargetType(workout_target_type_id=1, workout_target_type_key="no.target", display_order=1)


def create_warmup_step(step_id: int, step_order: int, end_condition: EndCondition, end_condition_value: Optional[float] = None) -> WorkoutStep:
    return WorkoutStep(
        step_id=step_id,
        step_order=step_order,
        step_type=StepType(step_type_id=1, step_type_key="warmup", display_order=1),
        end_condition=end_condition,
        target_type=create_no_target(),
        end_condition_value=end_condition_value
    )


def create_interval_step(step_id: int, step_order: int, end_condition: EndCondition, target_type: TargetType, 
                        end_condition_value: Optional[float] = None, target_value_one: Optional[float] = None, 
                        target_value_two: Optional[float] = None) -> WorkoutStep:
    return WorkoutStep(
        step_id=step_id,
        step_order=step_order,
        step_type=StepType(step_type_id=3, step_type_key="interval", display_order=3),
        end_condition=end_condition,
        target_type=target_type,
        end_condition_value=end_condition_value,
        target_value_one=target_value_one,
        target_value_two=target_value_two
    )


def create_cooldown_step(step_id: int, step_order: int, end_condition: EndCondition, end_condition_value: Optional[float] = None) -> WorkoutStep:
    return WorkoutStep(
        step_id=step_id,
        step_order=step_order,
        step_type=StepType(step_type_id=2, step_type_key="cooldown", display_order=2),
        end_condition=end_condition,
        target_type=create_no_target(),
        end_condition_value=end_condition_value
    )
