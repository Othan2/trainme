from typing import Dict, Any
from .models.user_profile import (
    UserProfile,
    UserData,
    UserSleep,
    Gender,
    TimeFormat,
    MeasurementSystem,
    Handedness,
    IntensityCalcMethod,
    GolfDistanceUnit,
    HydrationUnit,
    DayOfWeek,
    Format,
    FirstDayOfWeek,
    WeatherLocation,
)


class UserProfileParser:
    """Parser to convert Garmin API user profile JSON to UserProfile objects"""

    @staticmethod
    def _parse_format(format_data: Dict[str, Any]) -> Format:
        """Parse JSON format data to Format object. For power and heart rate format"""
        return Format(
            format_id=format_data.get("formatId", 0),
            format_key=format_data.get("formatKey", ""),
            min_fraction=format_data.get("minFraction", 0),
            max_fraction=format_data.get("maxFraction", 0),
            grouping_used=format_data.get("groupingUsed", False),
            display_format=format_data.get("displayFormat"),
        )

    @staticmethod
    def _parse_first_day_of_week(day_data: Dict[str, Any]) -> FirstDayOfWeek:
        """Parse JSON first day of week data to FirstDayOfWeek object"""
        return FirstDayOfWeek(
            day_id=day_data.get("dayId", 1),
            day_name=day_data.get("dayName", "monday"),
            sort_order=day_data.get("sortOrder", 1),
            is_possible_first_day=day_data.get("isPossibleFirstDay", True),
        )

    @staticmethod
    def _parse_weather_location(weather_data: Dict[str, Any]) -> WeatherLocation:
        """Parse JSON weather location data to WeatherLocation object"""
        return WeatherLocation(
            use_fixed_location=weather_data.get("useFixedLocation", False),
            latitude=weather_data.get("latitude"),
            longitude=weather_data.get("longitude"),
            location_name=weather_data.get("locationName"),
            iso_country_code=weather_data.get("isoCountryCode"),
            postal_code=weather_data.get("postalCode"),
        )

    @staticmethod
    def _parse_enum_list(enum_list: list, enum_class) -> list:
        """Parse list of enum strings to enum objects"""
        result = []
        for item in enum_list:
            try:
                result.append(enum_class(item))
            except ValueError:
                # Skip invalid enum values
                continue
        return result

    @staticmethod
    def _parse_user_data(user_data_json: Dict[str, Any]) -> UserData:
        """Parse JSON user data to UserData object"""
        # Parse enums with defaults
        gender = Gender(user_data_json.get("gender", "MALE"))
        time_format = TimeFormat(user_data_json.get("timeFormat", "time_twelve_hr"))
        measurement_system = MeasurementSystem(
            user_data_json.get("measurementSystem", "metric")
        )
        handedness = Handedness(user_data_json.get("handedness", "RIGHT"))
        intensity_calc_method = IntensityCalcMethod(
            user_data_json.get("intensityMinutesCalcMethod", "AUTO")
        )
        golf_distance_unit = GolfDistanceUnit(
            user_data_json.get("golfDistanceUnit", "metric")
        )
        hydration_unit = HydrationUnit(
            user_data_json.get("hydrationMeasurementUnit", "cup")
        )

        # Parse format objects
        power_format = UserProfileParser._parse_format(
            user_data_json.get("powerFormat", {})
        )
        heart_rate_format = UserProfileParser._parse_format(
            user_data_json.get("heartRateFormat", {})
        )
        first_day_of_week = UserProfileParser._parse_first_day_of_week(
            user_data_json.get("firstDayOfWeek", {})
        )
        weather_location = UserProfileParser._parse_weather_location(
            user_data_json.get("weatherLocation", {})
        )

        # Parse training days
        available_training_days = UserProfileParser._parse_enum_list(
            user_data_json.get("availableTrainingDays", []), DayOfWeek
        )
        preferred_long_training_days = UserProfileParser._parse_enum_list(
            user_data_json.get("preferredLongTrainingDays", []), DayOfWeek
        )

        return UserData(
            gender=gender,
            weight=user_data_json.get("weight", 0.0),
            height=user_data_json.get("height", 0.0),
            time_format=time_format,
            birth_date=user_data_json.get("birthDate", "1990-01-01"),
            measurement_system=measurement_system,
            activity_level=user_data_json.get("activityLevel"),
            handedness=handedness,
            power_format=power_format,
            heart_rate_format=heart_rate_format,
            first_day_of_week=first_day_of_week,
            vo2_max_running=user_data_json.get("vo2MaxRunning"),
            vo2_max_cycling=user_data_json.get("vo2MaxCycling"),
            lactate_threshold_speed=user_data_json.get("lactateThresholdSpeed"),
            lactate_threshold_heart_rate=user_data_json.get("lactateThresholdHeartRate"),
            dive_number=user_data_json.get("diveNumber"),
            intensity_minutes_calc_method=intensity_calc_method,
            moderate_intensity_minutes_hr_zone=user_data_json.get(
                "moderateIntensityMinutesHrZone", 3
            ),
            vigorous_intensity_minutes_hr_zone=user_data_json.get(
                "vigorousIntensityMinutesHrZone", 4
            ),
            hydration_measurement_unit=hydration_unit,
            hydration_containers=user_data_json.get("hydrationContainers", []),
            hydration_auto_goal_enabled=user_data_json.get(
                "hydrationAutoGoalEnabled", True
            ),
            firstbeat_max_stress_score=user_data_json.get("firstbeatMaxStressScore"),
            firstbeat_cycling_lt_timestamp=user_data_json.get(
                "firstbeatCyclingLtTimestamp"
            ),
            firstbeat_running_lt_timestamp=user_data_json.get(
                "firstbeatRunningLtTimestamp"
            ),
            threshold_heart_rate_auto_detected=user_data_json.get(
                "thresholdHeartRateAutoDetected", True
            ),
            ftp_auto_detected=user_data_json.get("ftpAutoDetected"),
            training_status_paused_date=user_data_json.get("trainingStatusPausedDate"),
            weather_location=weather_location,
            golf_distance_unit=golf_distance_unit,
            golf_elevation_unit=user_data_json.get("golfElevationUnit"),
            golf_speed_unit=user_data_json.get("golfSpeedUnit"),
            external_bottom_time=user_data_json.get("externalBottomTime"),
            available_training_days=available_training_days,
            preferred_long_training_days=preferred_long_training_days,
        )

    @staticmethod
    def _parse_user_sleep(sleep_data: Dict[str, Any]) -> UserSleep:
        """Parse JSON user sleep data to UserSleep object"""
        return UserSleep(
            sleep_time=sleep_data.get("sleepTime", 0),
            default_sleep_time=sleep_data.get("defaultSleepTime", False),
            wake_time=sleep_data.get("wakeTime", 0),
            default_wake_time=sleep_data.get("defaultWakeTime", False),
        )

    @staticmethod
    def parse_user_profile(profile_json: Dict[str, Any]) -> UserProfile:
        """Parse complete JSON user profile to UserProfile object"""
        user_data = UserProfileParser._parse_user_data(profile_json.get("userData", {}))
        user_sleep = UserProfileParser._parse_user_sleep(
            profile_json.get("userSleep", {})
        )

        return UserProfile(
            id=profile_json.get("id", 0),
            user_data=user_data,
            user_sleep=user_sleep,
            connect_date=profile_json.get("connectDate"),
            source_type=profile_json.get("sourceType"),
        )
