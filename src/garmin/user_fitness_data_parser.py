from typing import Dict, Any, List, Optional
from datetime import datetime, date
from .models.user_fitness_data import (
    UserFitnessData,
    Goal,
    TrainingAvailability,
    ActivitySummary,
    BodyBatteryData,
    SleepData,
    HeartRateData,
    StressData,
    TrainingReadinessData,
    EnduranceData,
    RacePredictionData,
    MaxMetricsData,
    TrainingStatusData,
    GoalsData,
    RecentActivitiesData,
)
from .models.user_profile import UserProfile


class UserFitnessDataParser:
    """Parser to convert raw Garmin API data to UserFitnessData objects"""

    @staticmethod
    def parse_body_battery(body_battery_data: List[Dict[str, Any]]) -> BodyBatteryData:
        """Parse body battery data from API response"""
        if not isinstance(body_battery_data, list):
            raise ValueError(
                f"Expected list for body battery data, got {type(body_battery_data)}"
            )

        body_battery = BodyBatteryData()

        if body_battery_data and len(body_battery_data) > 0:
            latest_bb = body_battery_data[-1]
            if not isinstance(latest_bb, dict):
                raise ValueError(
                    f"Expected dict for body battery entry, got {type(latest_bb)}"
                )

            body_battery.current_level = latest_bb.get("bodyBatteryValue")
            body_battery.charged_today = latest_bb.get("charged")
            body_battery.drained_today = latest_bb.get("drained")
            body_battery.highest_today = latest_bb.get("highestLevel")
            body_battery.lowest_today = latest_bb.get("lowestLevel")

        return body_battery

    @staticmethod
    def parse_sleep_data(sleep_data: Dict[str, Any]) -> SleepData:
        """Parse sleep data from API response"""
        if not isinstance(sleep_data, dict):
            raise ValueError(f"Expected dict for sleep data, got {type(sleep_data)}")

        sleep = SleepData()

        if sleep_data:
            sleep.total_sleep_hours = sleep_data.get("sleepTimeSeconds", 0) / 3600
            sleep.deep_sleep_hours = sleep_data.get("deepSleepSeconds", 0) / 3600
            sleep.light_sleep_hours = sleep_data.get("lightSleepSeconds", 0) / 3600
            sleep.rem_sleep_hours = sleep_data.get("remSleepSeconds", 0) / 3600
            sleep.awake_hours = sleep_data.get("awakeDuration", 0) / 3600
            sleep.sleep_score = sleep_data.get("sleepScore")
            sleep.sleep_start_time = sleep_data.get("sleepStartTimestampLocal")
            sleep.sleep_end_time = sleep_data.get("sleepEndTimestampLocal")

        return sleep

    @staticmethod
    def parse_heart_rate_data(
        rhr_data: Dict[str, Any], hrv_data: Dict[str, Any]
    ) -> HeartRateData:
        """Parse heart rate and HRV data from API responses"""
        if not isinstance(rhr_data, dict):
            raise ValueError(f"Expected dict for RHR data, got {type(rhr_data)}")
        if not isinstance(hrv_data, dict):
            raise ValueError(f"Expected dict for HRV data, got {type(hrv_data)}")

        heart_rate = HeartRateData()

        # Parse resting heart rate data
        if rhr_data and "allMetrics" in rhr_data:
            metrics_map = rhr_data["allMetrics"].get("metricsMap", {})
            for metric_values in metrics_map.values():
                if metric_values and len(metric_values) > 0:
                    heart_rate.resting_heart_rate = metric_values[0].get("value")
                    break

        # Parse HRV data
        if hrv_data:
            heart_rate.hrv_status = hrv_data.get("hrvStatus")
            heart_rate.hrv_seven_day_avg = hrv_data.get("sevenDayAvg")
            heart_rate.latest_hrv_value = hrv_data.get("lastNightValue")

        return heart_rate

    @staticmethod
    def parse_stress_data(stress_data: Dict[str, Any]) -> StressData:
        """Parse stress data from API response"""
        if not isinstance(stress_data, dict):
            raise ValueError(f"Expected dict for stress data, got {type(stress_data)}")

        stress = StressData()

        if stress_data:
            stress.current_stress_level = stress_data.get("overallStressLevel")
            stress.average_stress_today = stress_data.get("avgStressLevel")
            stress.max_stress_today = stress_data.get("maxStressLevel")
            stress.rest_stress_time_minutes = (
                stress_data.get("restStressDuration", 0) / 60
            )
            stress.low_stress_time_minutes = (
                stress_data.get("lowStressDuration", 0) / 60
            )
            stress.medium_stress_time_minutes = (
                stress_data.get("mediumStressDuration", 0) / 60
            )
            stress.high_stress_time_minutes = (
                stress_data.get("highStressDuration", 0) / 60
            )

        return stress

    @staticmethod
    def parse_training_readiness(
        training_readiness: List[Dict[str, Any]],
    ) -> TrainingReadinessData:
        """Parse training readiness data from API response"""
        if not isinstance(training_readiness, list):
            raise ValueError(
                f"Expected list for training readiness data, got {type(training_readiness)}"
            )

        readiness = TrainingReadinessData()

        if training_readiness and len(training_readiness) > 0:
            latest_readiness = training_readiness[0]
            if not isinstance(latest_readiness, dict):
                raise ValueError(
                    f"Expected dict for training readiness entry, got {type(latest_readiness)}"
                )

            readiness.readiness_score = latest_readiness.get("score")
            readiness.readiness_status = latest_readiness.get("status")
            readiness.fatigue_level = latest_readiness.get("fatigueLevel")
            readiness.recovery_advisor = latest_readiness.get("recoveryAdvisor")

        return readiness

    @staticmethod
    def parse_endurance_data(endurance_data: Dict[str, Any]) -> EnduranceData:
        """Parse endurance data from API response"""
        if not isinstance(endurance_data, dict):
            raise ValueError(
                f"Expected dict for endurance data, got {type(endurance_data)}"
            )

        endurance = EnduranceData()

        if endurance_data:
            endurance.endurance_score = endurance_data.get("enduranceScore")
            endurance.endurance_trend = endurance_data.get("trend")
            endurance.aerobic_base = endurance_data.get("aerobicBase")
            endurance.anaerobic_capacity = endurance_data.get("anaerobicCapacity")

        return endurance

    @staticmethod
    def parse_race_predictions(race_predictions: Any) -> RacePredictionData:
        """Parse race prediction data from API response"""
        if race_predictions is not None and not isinstance(
            race_predictions, (dict, list)
        ):
            raise ValueError(
                f"Expected dict or list for race predictions data, got {type(race_predictions)}"
            )

        predictions = RacePredictionData()

        if race_predictions:
            if isinstance(race_predictions, dict):
                # Handle new API format with raw time values
                predictions.time_5k_seconds = race_predictions.get("time5K")
                predictions.time_10k_seconds = race_predictions.get("time10K")
                predictions.time_half_marathon_seconds = race_predictions.get(
                    "timeHalfMarathon"
                )
                predictions.time_marathon_seconds = race_predictions.get("timeMarathon")
                predictions.calendar_date = race_predictions.get("calendarDate")
                predictions.from_calendar_date = race_predictions.get(
                    "fromCalendarDate"
                )
                predictions.to_calendar_date = race_predictions.get("toCalendarDate")

        return predictions

    @staticmethod
    def parse_max_metrics_data(max_metrics: Dict[str, Any]) -> MaxMetricsData:
        """Parse max metrics including VO2 Max and environmental acclimatization from API response"""
        if not isinstance(max_metrics, dict):
            raise ValueError(
                f"Expected dict for max metrics data, got {type(max_metrics)}"
            )

        metrics = MaxMetricsData()

        # Parse generic metrics (running)
        if max_metrics and max_metrics.get("generic"):
            generic_data = max_metrics["generic"]
            metrics.calendar_date = generic_data.get("calendarDate")
            metrics.vo2_max_precise_value = generic_data.get("vo2MaxPreciseValue")
            metrics.vo2_max_value = generic_data.get("vo2MaxValue")
            metrics.fitness_age = generic_data.get("fitnessAge")
            metrics.fitness_age_description = generic_data.get("fitnessAgeDescription")
            metrics.max_met_category = generic_data.get("maxMetCategory")

        # Parse cycling metrics
        if max_metrics.get("cycling"):
            cycling_data = max_metrics["cycling"]
            metrics.vo2_max_cycling = cycling_data.get("vo2MaxValue")

        # Parse heat and altitude acclimatization
        if max_metrics.get("heatAltitudeAcclimation"):
            accl_data = max_metrics["heatAltitudeAcclimation"]
            metrics.heat_altitude_calendar_date = accl_data.get("calendarDate")
            metrics.altitude_acclimatization_date = accl_data.get(
                "altitudeAcclimationDate"
            )
            metrics.previous_altitude_acclimatization_date = accl_data.get(
                "previousAltitudeAcclimationDate"
            )
            metrics.heat_acclimatization_date = accl_data.get("heatAcclimationDate")
            metrics.previous_heat_acclimatization_date = accl_data.get(
                "previousHeatAcclimationDate"
            )
            metrics.altitude_acclimatization = accl_data.get("altitudeAcclimation")
            metrics.previous_altitude_acclimatization = accl_data.get(
                "previousAltitudeAcclimation"
            )
            metrics.heat_acclimatization_percentage = accl_data.get(
                "heatAcclimationPercentage"
            )
            metrics.previous_heat_acclimatization_percentage = accl_data.get(
                "previousHeatAcclimationPercentage"
            )
            metrics.heat_trend = accl_data.get("heatTrend")
            metrics.altitude_trend = accl_data.get("altitudeTrend")
            metrics.current_altitude = accl_data.get("currentAltitude")
            metrics.previous_altitude = accl_data.get("previousAltitude")
            metrics.acclimatization_percentage = accl_data.get("acclimationPercentage")
            metrics.previous_acclimatization_percentage = accl_data.get(
                "previousAcclimationPercentage"
            )
            metrics.altitude_acclimatization_local_timestamp = accl_data.get(
                "altitudeAcclimationLocalTimestamp"
            )

        return metrics

    @staticmethod
    def parse_training_status(training_status: Dict[str, Any]) -> TrainingStatusData:
        """Parse training status data from API response"""
        if not isinstance(training_status, dict):
            raise ValueError(
                f"Expected dict for training status data, got {type(training_status)}"
            )

        status = TrainingStatusData()

        if training_status:
            # Handle new API structure with mostRecentTrainingStatus
            most_recent = training_status.get("mostRecentTrainingStatus", {})
            latest_data = most_recent.get("latestTrainingStatusData", {})

            # Get the first device's training status data
            device_data = None
            for _, data in latest_data.items():
                device_data = data
                break

            if device_data:
                # Map training status code to readable status
                training_status_code = device_data.get("trainingStatus")
                status_map = {
                    4: "MAINTAINING",
                }
                status.training_status = status_map.get(training_status_code, "UNKNOWN")

                # Get weekly training load
                status.current_training_load = device_data.get("weeklyTrainingLoad")

                # Get load tunnel for optimal training load
                load_min = device_data.get("loadTunnelMin")
                load_max = device_data.get("loadTunnelMax")
                if load_min and load_max:
                    status.optimal_training_load = f"{load_min}-{load_max}"

                # Get acute training load if available
                acute_dto = device_data.get("acuteTrainingLoadDTO")
                if acute_dto:
                    status.acute_load = acute_dto.get("acuteTrainingLoad")

            # Handle training load balance from mostRecentTrainingLoadBalance
            load_balance = training_status.get("mostRecentTrainingLoadBalance", {})
            metrics_map = load_balance.get("metricsTrainingLoadBalanceDTOMap", {})

            # Get the first device's load balance data
            if metrics_map:
                balance_data = next(iter(metrics_map.values()))

                feedback_phrase = balance_data.get("trainingBalanceFeedbackPhrase")
                if feedback_phrase:
                    status.training_load_balance = feedback_phrase.replace(
                        "_", " "
                    ).title()

                # Extract monthly load data
                status.monthly_load_aerobic_low = balance_data.get(
                    "monthlyLoadAerobicLow"
                )
                status.monthly_load_aerobic_high = balance_data.get(
                    "monthlyLoadAerobicHigh"
                )
                status.monthly_load_anaerobic = balance_data.get("monthlyLoadAnaerobic")
                status.monthly_load_aerobic_low_target_min = balance_data.get(
                    "monthlyLoadAerobicLowTargetMin"
                )
                status.monthly_load_aerobic_low_target_max = balance_data.get(
                    "monthlyLoadAerobicLowTargetMax"
                )
                status.monthly_load_aerobic_high_target_min = balance_data.get(
                    "monthlyLoadAerobicHighTargetMin"
                )
                status.monthly_load_aerobic_high_target_max = balance_data.get(
                    "monthlyLoadAerobicHighTargetMax"
                )
                status.monthly_load_anaerobic_target_min = balance_data.get(
                    "monthlyLoadAnaerobicTargetMin"
                )
                status.monthly_load_anaerobic_target_max = balance_data.get(
                    "monthlyLoadAnaerobicTargetMax"
                )

        return status

    @staticmethod
    def parse_goals_data(goals_data: List[Dict[str, Any]]) -> GoalsData:
        """Parse goals data from API response"""
        if not isinstance(goals_data, list):
            raise ValueError(f"Expected list for goals data, got {type(goals_data)}")

        goals = GoalsData()

        for goal_raw in goals_data:
            if not isinstance(goal_raw, dict):
                raise ValueError(f"Expected dict for goal entry, got {type(goal_raw)}")

            goal = Goal(
                goal_id=goal_raw.get("goalId", 0),
                goal_type=goal_raw.get("goalType", "unknown"),
                goal_name=goal_raw.get("goalName", "Unknown Goal"),
                target_value=goal_raw.get("targetValue"),
                target_date=goal_raw.get("targetDate"),
                current_progress=goal_raw.get("currentProgress"),
                status=goal_raw.get("status", "active"),
                activity_type=goal_raw.get("activityType"),
            )
            goals.active_goals.append(goal)

        return goals

    @staticmethod
    def parse_recent_activities_data(
        activities_raw: List[Dict[str, Any]], limit: int
    ) -> RecentActivitiesData:
        """Parse raw activities data to RecentActivitiesData object"""
        if not isinstance(activities_raw, list):
            raise ValueError(
                f"Expected list for activities data, got {type(activities_raw)}"
            )

        activities = []

        for activity_raw in activities_raw[:limit]:
            if not isinstance(activity_raw, dict):
                raise ValueError(
                    f"Expected dict for activity entry, got {type(activity_raw)}"
                )

            activity_summary = ActivitySummary(
                activity_id=activity_raw.get("activityId", 0),
                activity_name=activity_raw.get("activityName", "Unknown Activity"),
                activity_type=activity_raw.get("activityType", {}).get(
                    "typeKey", "unknown"
                ),
                start_time=activity_raw.get("startTimeLocal", ""),
                distance_meters=activity_raw.get("distance"),
                duration_seconds=activity_raw.get("duration", 0),
                average_pace_per_km=UserFitnessDataParser._calculate_pace(
                    activity_raw.get("distance"), activity_raw.get("duration")
                ),
                average_speed_kmh=UserFitnessDataParser._convert_speed_to_kmh(
                    activity_raw.get("averageSpeed")
                ),
                average_heart_rate=activity_raw.get("averageHR"),
                max_heart_rate=activity_raw.get("maxHR"),
                calories=activity_raw.get("calories"),
                training_effect_aerobic=activity_raw.get("aerobicTrainingEffect"),
                training_effect_anaerobic=activity_raw.get("anaerobicTrainingEffect"),
                training_load=activity_raw.get("activityTrainingLoad"),
                completion_status="completed",  # Assume completed if in activity list
            )
            activities.append(activity_summary)

        return RecentActivitiesData(activities=activities)

    @staticmethod
    def parse_training_availability(user_profile: UserProfile) -> TrainingAvailability:
        """Parse training availability from user profile"""
        if not isinstance(user_profile, UserProfile):
            raise ValueError(
                f"Expected UserProfile for user profile data, got {type(user_profile)}"
            )

        return TrainingAvailability(
            available_training_days=[
                day.value for day in user_profile.user_data.available_training_days
            ],
            preferred_long_training_days=[
                day.value for day in user_profile.user_data.preferred_long_training_days
            ],
            typical_training_duration_minutes=60,  # Default assumption
            max_training_duration_minutes=180,  # Default assumption
            preferred_training_time="morning",  # Default assumption
            training_frequency_per_week=len(
                user_profile.user_data.available_training_days
            ),
        )

    @staticmethod
    def _calculate_pace(
        distance_m: Optional[float], duration_s: Optional[float]
    ) -> Optional[str]:
        """Calculate pace in mm:ss per kilometer format"""
        if not distance_m or not duration_s or distance_m <= 0:
            return None

        try:
            pace_per_km_seconds = (duration_s / distance_m) * 1000
            minutes = int(pace_per_km_seconds // 60)
            seconds = int(pace_per_km_seconds % 60)
            return f"{minutes}:{seconds:02d}"
        except (ZeroDivisionError, ValueError):
            return None

    @staticmethod
    def _convert_speed_to_kmh(speed_ms: Optional[float]) -> Optional[float]:
        """Convert speed from m/s to km/h"""
        if speed_ms is None:
            return None
        return speed_ms * 3.6

    @staticmethod
    def _format_time_from_seconds(total_seconds: Optional[int]) -> Optional[str]:
        """Format time from seconds to HH:MM:SS or MM:SS format"""
        if total_seconds is None:
            return None

        try:
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60

            if hours > 0:
                return f"{hours}:{minutes:02d}:{seconds:02d}"
            else:
                return f"{minutes}:{seconds:02d}"
        except (ValueError, TypeError):
            return None
