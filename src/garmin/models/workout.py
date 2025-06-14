from typing import Optional, List, Dict, Any, Union, Literal
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field, Discriminator, field_validator
from typing import Annotated

class SportType(Enum):
    RUNNING = ("running", 1, 1)

    @classmethod
    def _missing_(cls, value):
        # Handle list inputs (from JSON serialization) by converting to tuple
        if isinstance(value, list) and len(value) == 3:
            value = tuple(value)
        for item in cls:
            if item.value == value:
                return item
        raise ValueError(f"{value} is not a valid {cls.__name__}")

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

    @classmethod
    def _missing_(cls, value):
        # Handle list inputs (from JSON serialization) by converting to tuple
        if isinstance(value, list) and len(value) == 3:
            value = tuple(value)
        for item in cls:
            if item.value == value:
                return item
        raise ValueError(f"{value} is not a valid {cls.__name__}")

    def to_dict(self) -> Dict[str, Any]:
        key, condition_id, display_order = self.value
        
        return {
            "conditionTypeId": condition_id,
            "conditionTypeKey": key,
            "displayOrder": display_order
        }


class EndCondition(BaseModel):
    condition_type: EndConditionType
    # Seconds for a time end condition. Meters for a distance or lap.button end condition.
    value: Annotated[float, Field(description="Time in seconds for a time end condition. Meters for a distance or lap.button end condition.")]
    displayable: bool = True

    def to_dict(self) -> Dict[str, Any]:
        condition_dict = self.condition_type.to_dict()
        condition_dict["displayable"] = self.displayable
        return condition_dict

    def __str__(self) -> str:
        if self.condition_type == EndConditionType.TIME:
            mins, secs = divmod(int(self.value), 60)
            return f"{mins}:{secs:02d}"
        elif self.condition_type == EndConditionType.DISTANCE:
            return f"{self.value}m"
        return f"{self.condition_type.value[0]}: {self.value}"


class IntensityTarget(BaseModel, ABC):
    @abstractmethod
    def to_target_dict(self) -> Dict[str, Any]:
        """Return the target type dictionary for API calls"""
        pass

class NoTarget(IntensityTarget):
    target_type: Literal["no_target"] = Field(default="no_target", description="Discriminator field")
    
    def to_target_dict(self) -> Dict[str, Any]:
        return {
            "workoutTargetTypeId": 1,
            "workoutTargetTypeKey": "no.target",
            "displayOrder": 1
        }

    def __str__(self) -> str:
        return "No target"

class CadenceTarget(IntensityTarget):
    target_type: Literal["cadence"] = Field(default="cadence", description="Discriminator field")
    lower_bound: int = Field(description="Lower bound steps per minute")
    upper_bound: int = Field(description="Upper bound steps per minute")
    target_value_unit: Optional[str] = None
    
    def model_post_init(self, __context) -> None:
        if self.lower_bound >= self.upper_bound:
            raise ValueError(f"Lower bound ({self.lower_bound}) must be less than upper bound ({self.upper_bound})")
    
    def to_target_dict(self) -> Dict[str, Any]:
        return {
            "workoutTargetTypeId": 3,
            "workoutTargetTypeKey": "cadence", 
            "displayOrder": 3
        }

    def __str__(self) -> str:
        return f"Cadence {self.lower_bound}-{self.upper_bound} spm"

class HeartRateZoneTarget(IntensityTarget):
    target_type: Literal["heart_rate_zone"] = Field(default="heart_rate_zone", description="Discriminator field")
    zone_number: Annotated[int, Field(description="Heart rate zone. 1 through 5.")]
    target_value_unit: Optional[str] = None
    
    def to_target_dict(self) -> Dict[str, Any]:
        return {
            "workoutTargetTypeId": 4,
            "workoutTargetTypeKey": "heart.rate.zone",
            "displayOrder": 4
        }

    def __str__(self) -> str:
        return f"HR Zone {self.zone_number}"

class PaceZoneTarget(IntensityTarget):
    target_type: Literal["pace_zone"] = Field(default="pace_zone", description="Discriminator field")
    lower_bound: Annotated[float, Field(description="Faster pace in zone to run at, in meters per second.")]
    upper_bound: Annotated[float, Field(description="Slower pace in zone to run at, in meters per second.")]
    target_value_unit: Optional[str] = None
    
    def model_post_init(self, __context) -> None:
        if self.lower_bound < self.upper_bound:
            raise ValueError(f"Pace lower bound ({self.lower_bound}) must be greater than upper bound ({self.upper_bound}) - it is measured in meters per second")
    
    def to_target_dict(self) -> Dict[str, Any]:
        return {
            "workoutTargetTypeId": 6,
            "workoutTargetTypeKey": "pace.zone",
            "displayOrder": 6
        }

    def __str__(self) -> str:
        # Convert from m/s to min/mile (1 mile = 1609.344 meters)
        upper_min_mile = (1609.344 / self.upper_bound) / 60
        lower_min_mile = (1609.344 / self.lower_bound) / 60
        
        def format_pace(pace_min_mile):
            mins = int(pace_min_mile)
            secs = int((pace_min_mile - mins) * 60)
            return f"{mins}:{secs:02d}"
        
        return f"Pace {format_pace(upper_min_mile)}-{format_pace(lower_min_mile)} min/mile"


class StepType(Enum):
    WARMUP = ("warmup", 1, 1)
    COOLDOWN = ("cooldown", 2, 2)
    INTERVAL = ("interval", 3, 3)
    RECOVERY = ("recovery", 4, 4)
    REST = ("rest", 5, 5)
    OTHER = ("other", 7, 7)

    @classmethod
    def _missing_(cls, value):
        # Handle list inputs (from JSON serialization) by converting to tuple
        if isinstance(value, list) and len(value) == 3:
            value = tuple(value)
        for item in cls:
            if item.value == value:
                return item
        raise ValueError(f"{value} is not a valid {cls.__name__}")

    def to_dict(self) -> Dict[str, Any]:
        key, step_id, display_order = self.value
        
        return {
            "stepTypeId": step_id,
            "stepTypeKey": key,
            "displayOrder": display_order
        }


IntensityTargetType = Annotated[
    Union[NoTarget, CadenceTarget, HeartRateZoneTarget, PaceZoneTarget],
    Field(discriminator='target_type')
]

class WorkoutStep(BaseModel):
    step_order: int
    step_type: StepType
    end_condition: Annotated[EndCondition, Field(description="Condition to determine when the workout step is complete.")]
    intensity: IntensityTargetType

    def __str__(self) -> str:
        return f"{self.step_type.value[0].title()}: {self.end_condition} @ {self.intensity}"
    
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


class WorkoutSegment(BaseModel):
    segment_order: int
    sport_type: SportType
    workout_steps: Annotated[List[WorkoutStep], Field(description="Individual steps in the workout to complete.")]

    def __str__(self) -> str:
        steps_str = "\n    ".join(str(step) for step in self.workout_steps)
        return f"  {self.sport_type.value[0].title()} Segment:\n    {steps_str}"

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
class Author:
    user_profile_pk: Optional[int] = None
    display_name: Optional[str] = None
    full_name: Optional[str] = None
    profile_img_name_large: Optional[str] = None
    profile_img_name_medium: Optional[str] = None
    profile_img_name_small: Optional[str] = None
    user_pro: bool = False
    vivokid_user: bool = False

@dataclass
class EstimatedDistanceUnit:
    unit_key: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {"unitKey": self.unit_key}


@dataclass
class WorkoutOverview:
    """Represents a workout overview as returned by Garmin Connect API"""
    workout_id: int
    owner_id: int
    workout_name: str
    sport_type: SportType
    update_date: str
    created_date: str
    author: Author
    shared: bool
    estimated: bool
    description: Optional[str] = None
    training_plan_id: Optional[int] = None
    estimated_duration_in_secs: Optional[int] = None
    estimated_distance_in_meters: Optional[float] = None
    estimate_type: Optional[str] = None
    estimated_distance_unit: Optional[EstimatedDistanceUnit] = None
    pool_length: float = 0.0
    pool_length_unit: Optional[EstimatedDistanceUnit] = None
    workout_provider: Optional[str] = None
    workout_source_id: Optional[str] = None
    consumer: Optional[str] = None
    atp_plan_id: Optional[int] = None
    workout_name_i18n_key: Optional[str] = None
    description_i18n_key: Optional[str] = None
    workout_thumbnail_url: Optional[str] = None
    
    def __str__(self) -> str:
        author_name = self.author.display_name or self.author.full_name or "Unknown"
        provider = f" ({self.workout_provider})" if self.workout_provider else ""
        return f"{self.workout_name} by {author_name}. Workout provider: {provider}. ID: {self.workout_id}"

class WorkoutDetail(ABC, BaseModel):
    """Base class for all workout types"""
    workout_name: str = Field(description="Name of the workout.")
    # Workout segments could be multiple types of activity, not just running. May want to allow that
    workout_segments: List[WorkoutSegment] =  Field(description="List of individual workout segments. Each activity type in the workout needs its own segment.")
    workout_source_id: Optional[str]= Field(default=None, description="Unique id for source of the training plan.")
    training_plan_id: Optional[str] = Field(default=None, description="Unique identifier of the training plan.")
    is_wheelchair: bool = False
    

    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convert the workout to a dictionary representation for Garmin API calls"""
        pass


from .run_workout import RunWorkout

# Union type for all concrete workout types
WorkoutDetailType = Union[RunWorkout]
