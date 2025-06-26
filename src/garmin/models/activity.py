from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field


class ActivityType(Enum):
    RUNNING = ("running", 1, 17)

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
        key, type_id, parent_type_id = self.value

        return {
            "typeId": type_id,
            "typeKey": key,
            "parentTypeId": parent_type_id,
            "isHidden": False,
            "restricted": False,
            "trimmable": True,
        }


class EventType(Enum):
    UNCATEGORIZED = ("uncategorized", 9, 10)

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
        key, type_id, sort_order = self.value

        return {"typeId": type_id, "typeKey": key, "sortOrder": sort_order}


class PrivacyType(Enum):
    PRIVATE = ("private", 2)
    PUBLIC = ("public", 1)

    @classmethod
    def _missing_(cls, value):
        # Handle list inputs (from JSON serialization) by converting to tuple
        if isinstance(value, list) and len(value) == 2:
            value = tuple(value)
        for item in cls:
            if item.value == value:
                return item
        raise ValueError(f"{value} is not a valid {cls.__name__}")

    def to_dict(self) -> Dict[str, Any]:
        key, type_id = self.value

        return {"typeId": type_id, "typeKey": key}


@dataclass
class SplitSummary:
    no_of_splits: int
    total_ascent: float
    duration: float
    split_type: str
    num_climb_sends: int
    max_elevation_gain: float
    average_elevation_gain: float
    max_distance: float
    distance: float
    average_speed: float
    max_speed: float
    num_falls: int
    elevation_loss: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "noOfSplits": self.no_of_splits,
            "totalAscent": self.total_ascent,
            "duration": self.duration,
            "splitType": self.split_type,
            "numClimbSends": self.num_climb_sends,
            "maxElevationGain": self.max_elevation_gain,
            "averageElevationGain": self.average_elevation_gain,
            "maxDistance": self.max_distance,
            "distance": self.distance,
            "averageSpeed": self.average_speed,
            "maxSpeed": self.max_speed,
            "numFalls": self.num_falls,
            "elevationLoss": self.elevation_loss,
        }


class Activity(BaseModel):
    activity_id: int = Field(description="Unique identifier for the activity")
    activity_name: str = Field(description="Name of the activity")
    start_time_local: str = Field(description="Local start time of the activity")
    start_time_gmt: str = Field(description="GMT start time of the activity")
    end_time_gmt: Optional[str] = Field(
        default=None, description="GMT end time of the activity"
    )

    activity_type: ActivityType = Field(description="Type of activity")
    event_type: EventType = Field(description="Event type")

    # Distance and duration
    distance: float = Field(description="Distance in meters")
    duration: float = Field(description="Duration in seconds")
    elapsed_duration: Optional[float] = Field(
        default=None, description="Elapsed duration in seconds"
    )
    moving_duration: Optional[float] = Field(
        default=None, description="Moving duration in seconds"
    )

    # Elevation
    elevation_gain: Optional[float] = Field(
        default=None, description="Elevation gain in meters"
    )
    elevation_loss: Optional[float] = Field(
        default=None, description="Elevation loss in meters"
    )
    min_elevation: Optional[float] = Field(
        default=None, description="Minimum elevation in meters"
    )
    max_elevation: Optional[float] = Field(
        default=None, description="Maximum elevation in meters"
    )

    # Speed
    average_speed: Optional[float] = Field(
        default=None, description="Average speed in m/s"
    )
    max_speed: Optional[float] = Field(default=None, description="Maximum speed in m/s")
    max_vertical_speed: Optional[float] = Field(
        default=None, description="Maximum vertical speed"
    )

    # Location
    start_latitude: Optional[float] = Field(
        default=None, description="Starting latitude"
    )
    start_longitude: Optional[float] = Field(
        default=None, description="Starting longitude"
    )
    end_latitude: Optional[float] = Field(default=None, description="Ending latitude")
    end_longitude: Optional[float] = Field(default=None, description="Ending longitude")
    location_name: Optional[str] = Field(default=None, description="Location name")

    # Owner info
    owner_id: int = Field(description="Owner's user ID")
    owner_display_name: str = Field(description="Owner's display name")
    owner_full_name: str = Field(description="Owner's full name")
    owner_profile_image_url_small: Optional[str] = Field(
        default=None, description="Small profile image URL"
    )
    owner_profile_image_url_medium: Optional[str] = Field(
        default=None, description="Medium profile image URL"
    )
    owner_profile_image_url_large: Optional[str] = Field(
        default=None, description="Large profile image URL"
    )

    # Health metrics
    calories: Optional[float] = Field(default=None, description="Calories burned")
    bmr_calories: Optional[float] = Field(default=None, description="BMR calories")
    average_hr: Optional[float] = Field(default=None, description="Average heart rate")
    max_hr: Optional[float] = Field(default=None, description="Maximum heart rate")

    # Running specific
    average_running_cadence_in_steps_per_minute: Optional[float] = Field(
        default=None, description="Average cadence"
    )
    max_running_cadence_in_steps_per_minute: Optional[float] = Field(
        default=None, description="Maximum cadence"
    )
    max_double_cadence: Optional[float] = Field(
        default=None, description="Maximum double cadence"
    )
    steps: Optional[int] = Field(default=None, description="Total steps")
    avg_stride_length: Optional[float] = Field(
        default=None, description="Average stride length"
    )

    # Additional metrics
    privacy: PrivacyType = Field(description="Privacy setting")
    sport_type_id: int = Field(description="Sport type ID")
    time_zone_id: Optional[int] = Field(default=None, description="Time zone ID")
    begin_timestamp: Optional[int] = Field(default=None, description="Begin timestamp")
    device_id: Optional[int] = Field(default=None, description="Device ID")
    manufacturer: Optional[str] = Field(default=None, description="Device manufacturer")

    # Training effects
    aerobic_training_effect: Optional[float] = Field(
        default=None, description="Aerobic training effect"
    )
    anaerobic_training_effect: Optional[float] = Field(
        default=None, description="Anaerobic training effect"
    )
    aerobic_training_effect_message: Optional[str] = Field(
        default=None, description="Aerobic training effect message"
    )
    anaerobic_training_effect_message: Optional[str] = Field(
        default=None, description="Anaerobic training effect message"
    )
    training_effect_label: Optional[str] = Field(
        default=None, description="Training effect label"
    )
    activity_training_load: Optional[float] = Field(
        default=None, description="Activity training load"
    )

    # Environmental
    min_temperature: Optional[float] = Field(
        default=None, description="Minimum temperature"
    )
    max_temperature: Optional[float] = Field(
        default=None, description="Maximum temperature"
    )
    water_estimated: Optional[float] = Field(
        default=None, description="Estimated water consumption"
    )

    # Performance metrics
    vo2_max_value: Optional[float] = Field(default=None, description="VO2 max value")
    fastest_split_1000: Optional[float] = Field(
        default=None, description="Fastest 1000m split time"
    )
    fastest_split_1609: Optional[float] = Field(
        default=None, description="Fastest mile split time"
    )

    # Heart rate zones
    hr_time_in_zone_1: Optional[float] = Field(
        default=None, description="Time in HR zone 1"
    )
    hr_time_in_zone_2: Optional[float] = Field(
        default=None, description="Time in HR zone 2"
    )
    hr_time_in_zone_3: Optional[float] = Field(
        default=None, description="Time in HR zone 3"
    )
    hr_time_in_zone_4: Optional[float] = Field(
        default=None, description="Time in HR zone 4"
    )
    hr_time_in_zone_5: Optional[float] = Field(
        default=None, description="Time in HR zone 5"
    )

    # Intensity minutes
    moderate_intensity_minutes: Optional[int] = Field(
        default=None, description="Moderate intensity minutes"
    )
    vigorous_intensity_minutes: Optional[int] = Field(
        default=None, description="Vigorous intensity minutes"
    )

    # Lap and split data
    lap_count: Optional[int] = Field(default=None, description="Number of laps")
    min_activity_lap_duration: Optional[float] = Field(
        default=None, description="Minimum lap duration"
    )
    split_summaries: Optional[List[SplitSummary]] = Field(
        default=None, description="Split summaries"
    )
    has_splits: bool = Field(default=False, description="Whether activity has splits")

    # Flags
    has_polyline: bool = Field(
        default=False, description="Whether activity has GPS polyline"
    )
    has_images: bool = Field(default=False, description="Whether activity has images")
    has_video: bool = Field(default=False, description="Whether activity has video")
    has_heat_map: bool = Field(
        default=False, description="Whether activity has heat map"
    )
    user_pro: bool = Field(default=False, description="Whether user is pro")
    purposeful: bool = Field(
        default=False, description="Whether activity is purposeful"
    )
    manual_activity: bool = Field(
        default=False, description="Whether activity was manually entered"
    )
    auto_calc_calories: bool = Field(
        default=False, description="Whether calories were auto-calculated"
    )
    elevation_corrected: bool = Field(
        default=False, description="Whether elevation was corrected"
    )
    atp_activity: bool = Field(
        default=False, description="Whether it's an ATP activity"
    )
    favorite: bool = Field(default=False, description="Whether activity is favorited")
    pr: bool = Field(default=False, description="Whether activity is a personal record")
    parent: bool = Field(
        default=False, description="Whether activity is a parent activity"
    )

    # Additional data
    user_roles: Optional[List[str]] = Field(default=None, description="User roles")

    def to_dict(self) -> Dict[str, Any]:
        """Convert activity to dictionary for API serialization"""
        result = {
            "activityId": self.activity_id,
            "activityName": self.activity_name,
            "startTimeLocal": self.start_time_local,
            "startTimeGMT": self.start_time_gmt,
            "activityType": self.activity_type.to_dict(),
            "eventType": self.event_type.to_dict(),
            "distance": self.distance,
            "duration": self.duration,
            "ownerId": self.owner_id,
            "ownerDisplayName": self.owner_display_name,
            "ownerFullName": self.owner_full_name,
            "privacy": self.privacy.to_dict(),
            "sportTypeId": self.sport_type_id,
            "hasPolyline": self.has_polyline,
            "hasImages": self.has_images,
            "hasVideo": self.has_video,
            "userPro": self.user_pro,
            "purposeful": self.purposeful,
            "manualActivity": self.manual_activity,
            "autoCalcCalories": self.auto_calc_calories,
            "elevationCorrected": self.elevation_corrected,
            "atpActivity": self.atp_activity,
            "favorite": self.favorite,
            "pr": self.pr,
            "parent": self.parent,
        }

        # Add optional fields if they exist
        optional_fields = [
            ("endTimeGMT", self.end_time_gmt),
            ("elapsedDuration", self.elapsed_duration),
            ("movingDuration", self.moving_duration),
            ("elevationGain", self.elevation_gain),
            ("elevationLoss", self.elevation_loss),
            ("minElevation", self.min_elevation),
            ("maxElevation", self.max_elevation),
            ("averageSpeed", self.average_speed),
            ("maxSpeed", self.max_speed),
            ("maxVerticalSpeed", self.max_vertical_speed),
            ("startLatitude", self.start_latitude),
            ("startLongitude", self.start_longitude),
            ("endLatitude", self.end_latitude),
            ("endLongitude", self.end_longitude),
            ("locationName", self.location_name),
            ("ownerProfileImageUrlSmall", self.owner_profile_image_url_small),
            ("ownerProfileImageUrlMedium", self.owner_profile_image_url_medium),
            ("ownerProfileImageUrlLarge", self.owner_profile_image_url_large),
            ("calories", self.calories),
            ("bmrCalories", self.bmr_calories),
            ("averageHR", self.average_hr),
            ("maxHR", self.max_hr),
            (
                "averageRunningCadenceInStepsPerMinute",
                self.average_running_cadence_in_steps_per_minute,
            ),
            (
                "maxRunningCadenceInStepsPerMinute",
                self.max_running_cadence_in_steps_per_minute,
            ),
            ("maxDoubleCadence", self.max_double_cadence),
            ("steps", self.steps),
            ("avgStrideLength", self.avg_stride_length),
            ("timeZoneId", self.time_zone_id),
            ("beginTimestamp", self.begin_timestamp),
            ("deviceId", self.device_id),
            ("manufacturer", self.manufacturer),
            ("aerobicTrainingEffect", self.aerobic_training_effect),
            ("anaerobicTrainingEffect", self.anaerobic_training_effect),
            ("aerobicTrainingEffectMessage", self.aerobic_training_effect_message),
            ("anaerobicTrainingEffectMessage", self.anaerobic_training_effect_message),
            ("trainingEffectLabel", self.training_effect_label),
            ("activityTrainingLoad", self.activity_training_load),
            ("minTemperature", self.min_temperature),
            ("maxTemperature", self.max_temperature),
            ("waterEstimated", self.water_estimated),
            ("vO2MaxValue", self.vo2_max_value),
            ("fastestSplit_1000", self.fastest_split_1000),
            ("fastestSplit_1609", self.fastest_split_1609),
            ("hrTimeInZone_1", self.hr_time_in_zone_1),
            ("hrTimeInZone_2", self.hr_time_in_zone_2),
            ("hrTimeInZone_3", self.hr_time_in_zone_3),
            ("hrTimeInZone_4", self.hr_time_in_zone_4),
            ("hrTimeInZone_5", self.hr_time_in_zone_5),
            ("moderateIntensityMinutes", self.moderate_intensity_minutes),
            ("vigorousIntensityMinutes", self.vigorous_intensity_minutes),
            ("lapCount", self.lap_count),
            ("minActivityLapDuration", self.min_activity_lap_duration),
            ("hasSplits", self.has_splits),
            ("hasHeatMap", self.has_heat_map),
            ("userRoles", self.user_roles),
        ]

        for field_name, field_value in optional_fields:
            if field_value is not None:
                result[field_name] = field_value

        if self.split_summaries:
            result["splitSummaries"] = [
                split.to_dict() for split in self.split_summaries
            ]

        return result

    def __str__(self) -> str:
        duration_mins = int(self.duration // 60)
        duration_secs = int(self.duration % 60)
        distance_km = self.distance / 1000

        return f"{self.activity_name}: {distance_km:.2f}km in {duration_mins}:{duration_secs:02d} on {self.start_time_local}"
