from typing import Optional, List, Dict, Any, Literal
from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime


class Gender(Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"


class TimeFormat(Enum):
    TWELVE_HOUR = "time_twelve_hr"
    TWENTY_FOUR_HOUR = "time_twenty_four_hr"


class MeasurementSystem(Enum):
    METRIC = "metric"
    STATUTE_US = "statute_us"


class Handedness(Enum):
    RIGHT = "RIGHT"
    LEFT = "LEFT"


class IntensityCalcMethod(Enum):
    AUTO = "AUTO"
    MANUAL = "MANUAL"


class GolfDistanceUnit(Enum):
    METRIC = "metric"
    STATUTE_US = "statute_us"


class HydrationUnit(Enum):
    CUP = "cup"
    FLUID_OUNCE = "fluid_ounce"
    MILLILITER = "milliliter"


class DayOfWeek(Enum):
    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
    SATURDAY = "SATURDAY"
    SUNDAY = "SUNDAY"


class Format(BaseModel):
    format_id: int
    format_key: str
    min_fraction: int
    max_fraction: int
    grouping_used: bool
    display_format: Optional[str] = None


class FirstDayOfWeek(BaseModel):
    day_id: int
    day_name: str
    sort_order: int
    is_possible_first_day: bool


class WeatherLocation(BaseModel):
    use_fixed_location: bool
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    location_name: Optional[str] = None
    iso_country_code: Optional[str] = None
    postal_code: Optional[str] = None


class UserData(BaseModel):
    gender: Gender
    weight: float = Field(description="Weight in grams")
    height: float = Field(description="Height in centimeters")
    time_format: TimeFormat
    birth_date: str = Field(description="Birth date in YYYY-MM-DD format")
    measurement_system: MeasurementSystem
    activity_level: Optional[int] = None
    handedness: Handedness
    power_format: Format
    heart_rate_format: Format
    first_day_of_week: FirstDayOfWeek
    vo2_max_running: Optional[float] = None
    vo2_max_cycling: Optional[float] = None
    lactate_threshold_speed: Optional[float] = Field(
        default=None, description="Speed in meters per second"
    )
    lactate_threshold_heart_rate: Optional[int] = None
    dive_number: Optional[int] = None
    intensity_minutes_calc_method: IntensityCalcMethod
    moderate_intensity_minutes_hr_zone: int
    vigorous_intensity_minutes_hr_zone: int
    hydration_measurement_unit: HydrationUnit
    hydration_containers: List[Any] = Field(default_factory=list)
    hydration_auto_goal_enabled: bool
    firstbeat_max_stress_score: Optional[float] = None
    firstbeat_cycling_lt_timestamp: Optional[int] = None
    firstbeat_running_lt_timestamp: Optional[int] = None
    threshold_heart_rate_auto_detected: bool
    ftp_auto_detected: Optional[bool] = None
    training_status_paused_date: Optional[str] = None
    weather_location: WeatherLocation
    golf_distance_unit: GolfDistanceUnit
    golf_elevation_unit: Optional[str] = None
    golf_speed_unit: Optional[str] = None
    external_bottom_time: Optional[str] = None
    available_training_days: List[DayOfWeek]
    preferred_long_training_days: List[DayOfWeek]


class UserSleep(BaseModel):
    sleep_time: int = Field(description="Sleep time in seconds from midnight")
    default_sleep_time: bool
    wake_time: int = Field(description="Wake time in seconds from midnight")
    default_wake_time: bool


class UserProfile(BaseModel):
    id: int
    user_data: UserData
    user_sleep: UserSleep
    connect_date: Optional[str] = None
    source_type: Optional[str] = None

    def __str__(self) -> str:
        # Calculate age from birth date
        birth_year = int(self.user_data.birth_date.split("-")[0])
        current_year = datetime.now().year
        age = current_year - birth_year

        # Convert weight and height to readable units
        weight_kg = self.user_data.weight / 1000
        height_cm = self.user_data.height

        fitness_data = [
            f"Age: {age}",
            f"Gender: {self.user_data.gender.value}",
            f"Weight: {weight_kg:.1f}kg",
            f"Height: {height_cm:.0f}cm",
            f"Measurement System: {self.user_data.measurement_system.value}",
            f"First Day of Week: {self.user_data.first_day_of_week.day_name}",
        ]

        # Add VO2 max data if available
        if self.user_data.vo2_max_running:
            fitness_data.append(
                f"VO2 Max Running: {self.user_data.vo2_max_running:.1f}"
            )
        if self.user_data.vo2_max_cycling:
            fitness_data.append(
                f"VO2 Max Cycling: {self.user_data.vo2_max_cycling:.1f}"
            )

        # Add lactate threshold data if available
        if self.user_data.lactate_threshold_speed:
            lt_speed_kmh = self.user_data.lactate_threshold_speed * 3.6
            fitness_data.append(f"LT Speed: {lt_speed_kmh:.1f}km/h")
        if self.user_data.lactate_threshold_heart_rate:
            fitness_data.append(
                f"LT Heart Rate: {self.user_data.lactate_threshold_heart_rate}bpm"
            )

        # Add activity level if available
        if self.user_data.activity_level:
            fitness_data.append(f"Activity Level: {self.user_data.activity_level}")

        # Add training availability
        training_days = [day.value for day in self.user_data.available_training_days]
        long_days = [day.value for day in self.user_data.preferred_long_training_days]

        if training_days:
            fitness_data.append(f"Available Training Days: {', '.join(training_days)}")
        if long_days:
            fitness_data.append(f"Preferred Long Training Days: {', '.join(long_days)}")

        return "User Fitness Profile:\n" + "\n".join(
            [f"  {data}" for data in fitness_data]
        )
