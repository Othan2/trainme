from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

from .user_profile import UserProfile


class Goal(BaseModel):
    """Training goal information"""

    goal_id: int = Field(description="Unique goal identifier")
    goal_type: str = Field(description="Type of goal (distance, time, event, etc.)")
    goal_name: str = Field(description="Goal name or description")
    target_value: Optional[float] = Field(
        default=None, description="Target value for the goal"
    )
    target_date: Optional[str] = Field(
        default=None, description="Target completion date"
    )
    current_progress: Optional[float] = Field(
        default=None, description="Current progress towards goal"
    )
    status: str = Field(description="Goal status (active, completed, paused, etc.)")
    activity_type: Optional[str] = Field(
        default=None, description="Associated activity type"
    )


class TrainingAvailability(BaseModel):
    """Training schedule and availability information"""

    available_training_days: List[str] = Field(
        description="Days available for training"
    )
    preferred_long_training_days: List[str] = Field(
        description="Preferred days for long workouts"
    )
    typical_training_duration_minutes: Optional[int] = Field(
        default=None, description="Typical training duration in minutes"
    )
    max_training_duration_minutes: Optional[int] = Field(
        default=None, description="Maximum training duration in minutes"
    )
    preferred_training_time: Optional[str] = Field(
        default=None, description="Preferred time of day for training"
    )
    training_frequency_per_week: Optional[int] = Field(
        default=None, description="Preferred training frequency per week"
    )


class ActivitySummary(BaseModel):
    """Summary of recent activity"""

    activity_id: int = Field(description="Activity ID")
    activity_name: str = Field(description="Activity name")
    activity_type: str = Field(description="Activity type (running, cycling, etc.)")
    start_time: str = Field(description="Activity start time")
    distance_meters: Optional[float] = Field(
        default=None, description="Distance in meters"
    )
    duration_seconds: float = Field(description="Duration in seconds")
    average_pace_per_km: Optional[str] = Field(
        default=None, description="Average pace per km (mm:ss)"
    )
    average_speed_kmh: Optional[float] = Field(
        default=None, description="Average speed in km/h"
    )
    average_heart_rate: Optional[int] = Field(
        default=None, description="Average heart rate"
    )
    max_heart_rate: Optional[int] = Field(
        default=None, description="Maximum heart rate"
    )
    calories: Optional[float] = Field(default=None, description="Calories burned")
    training_effect_aerobic: Optional[float] = Field(
        default=None, description="Aerobic training effect"
    )
    training_effect_anaerobic: Optional[float] = Field(
        default=None, description="Anaerobic training effect"
    )
    training_load: Optional[float] = Field(
        default=None, description="Activity training load"
    )
    completion_status: str = Field(
        description="Completion status (completed, abandoned, etc.)"
    )


class BodyBatteryData(BaseModel):
    """Body battery specific metrics"""

    current_level: Optional[float] = Field(
        default=None, description="Current body battery level (0-100)"
    )
    charged_today: Optional[float] = Field(
        default=None, description="Body battery charged during last sleep"
    )
    drained_today: Optional[float] = Field(
        default=None, description="Body battery drained during day"
    )
    highest_today: Optional[float] = Field(
        default=None, description="Highest body battery level today"
    )
    lowest_today: Optional[float] = Field(
        default=None, description="Lowest body battery level today"
    )


class SleepData(BaseModel):
    """Sleep metrics and quality"""

    total_sleep_hours: Optional[float] = Field(
        default=None, description="Total sleep duration in hours"
    )
    deep_sleep_hours: Optional[float] = Field(
        default=None, description="Deep sleep duration in hours"
    )
    light_sleep_hours: Optional[float] = Field(
        default=None, description="Light sleep duration in hours"
    )
    rem_sleep_hours: Optional[float] = Field(
        default=None, description="REM sleep duration in hours"
    )
    awake_hours: Optional[float] = Field(
        default=None, description="Time awake during sleep period in hours"
    )
    sleep_score: Optional[float] = Field(
        default=None, description="Overall sleep score"
    )
    sleep_start_time: Optional[str] = Field(
        default=None, description="Sleep start time"
    )
    sleep_end_time: Optional[str] = Field(default=None, description="Sleep end time")


class HeartRateData(BaseModel):
    """Heart rate related metrics"""

    resting_heart_rate: Optional[int] = Field(
        default=None, description="Current resting heart rate"
    )
    max_heart_rate: Optional[int] = Field(
        default=None, description="Maximum recorded heart rate"
    )
    hrv_status: Optional[str] = Field(
        default=None, description="HRV status (BALANCED, UNBALANCED, etc.)"
    )
    hrv_seven_day_avg: Optional[float] = Field(
        default=None, description="7-day average HRV"
    )
    latest_hrv_value: Optional[float] = Field(
        default=None, description="Most recent HRV measurement"
    )


class StressData(BaseModel):
    """Stress and recovery indicators"""

    current_stress_level: Optional[int] = Field(
        default=None, description="Current stress level (0-100)"
    )
    average_stress_today: Optional[int] = Field(
        default=None, description="Average stress level today"
    )
    max_stress_today: Optional[int] = Field(
        default=None, description="Maximum stress level today"
    )
    rest_stress_time_minutes: Optional[int] = Field(
        default=None, description="Time in rest stress today"
    )
    low_stress_time_minutes: Optional[int] = Field(
        default=None, description="Time in low stress today"
    )
    medium_stress_time_minutes: Optional[int] = Field(
        default=None, description="Time in medium stress today"
    )
    high_stress_time_minutes: Optional[int] = Field(
        default=None, description="Time in high stress today"
    )


class TrainingReadinessData(BaseModel):
    """Training readiness metrics"""

    readiness_score: Optional[float] = Field(
        default=None, description="Overall training readiness score"
    )
    readiness_status: Optional[str] = Field(
        default=None, description="Readiness status description"
    )
    fatigue_level: Optional[str] = Field(
        default=None, description="Current fatigue level"
    )
    recovery_advisor: Optional[str] = Field(default=None, description="Recovery advice")


class EnduranceData(BaseModel):
    """Endurance and aerobic fitness metrics"""

    endurance_score: Optional[float] = Field(
        default=None, description="Current endurance score"
    )
    endurance_trend: Optional[str] = Field(
        default=None, description="Endurance trend (improving, maintaining, declining)"
    )
    aerobic_base: Optional[float] = Field(
        default=None, description="Aerobic base score"
    )
    anaerobic_capacity: Optional[float] = Field(
        default=None, description="Anaerobic capacity score"
    )


class RacePredictionData(BaseModel):
    """Race time predictions"""

    # Raw time values in seconds
    time_5k_seconds: Optional[int] = Field(
        default=None, description="5K prediction time in seconds"
    )
    time_10k_seconds: Optional[int] = Field(
        default=None, description="10K prediction time in seconds"
    )
    time_half_marathon_seconds: Optional[int] = Field(
        default=None, description="Half marathon prediction time in seconds"
    )
    time_marathon_seconds: Optional[int] = Field(
        default=None, description="Marathon prediction time in seconds"
    )

    # Date information
    calendar_date: Optional[str] = Field(
        default=None, description="Calendar date of predictions"
    )
    from_calendar_date: Optional[str] = Field(
        default=None, description="From calendar date"
    )
    to_calendar_date: Optional[str] = Field(
        default=None, description="To calendar date"
    )


class MaxMetricsData(BaseModel):
    """Max metrics including VO2 Max and environmental acclimatization"""

    # Generic metrics (running)
    calendar_date: Optional[str] = Field(
        default=None, description="Date of the VO2 max measurement"
    )
    vo2_max_precise_value: Optional[float] = Field(
        default=None, description="Precise VO2 max value for running"
    )
    vo2_max_value: Optional[float] = Field(
        default=None, description="Rounded VO2 max value for running"
    )
    fitness_age: Optional[int] = Field(default=None, description="Fitness age in years")
    fitness_age_description: Optional[str] = Field(
        default=None, description="Fitness age description"
    )
    max_met_category: Optional[int] = Field(
        default=None, description="Max MET category"
    )

    # Cycling metrics
    vo2_max_cycling: Optional[float] = Field(
        default=None, description="VO2 max for cycling"
    )

    # Heat and altitude acclimatization
    heat_altitude_calendar_date: Optional[str] = Field(
        default=None, description="Calendar date for heat/altitude data"
    )
    altitude_acclimatization_date: Optional[str] = Field(
        default=None, description="Current altitude acclimatization date"
    )
    previous_altitude_acclimatization_date: Optional[str] = Field(
        default=None, description="Previous altitude acclimatization date"
    )
    heat_acclimatization_date: Optional[str] = Field(
        default=None, description="Current heat acclimatization date"
    )
    previous_heat_acclimatization_date: Optional[str] = Field(
        default=None, description="Previous heat acclimatization date"
    )
    altitude_acclimatization: Optional[int] = Field(
        default=None, description="Current altitude acclimatization level"
    )
    previous_altitude_acclimatization: Optional[int] = Field(
        default=None, description="Previous altitude acclimatization level"
    )
    heat_acclimatization_percentage: Optional[int] = Field(
        default=None, description="Current heat acclimatization percentage"
    )
    previous_heat_acclimatization_percentage: Optional[int] = Field(
        default=None, description="Previous heat acclimatization percentage"
    )
    heat_trend: Optional[str] = Field(
        default=None, description="Heat acclimatization trend"
    )
    altitude_trend: Optional[str] = Field(
        default=None, description="Altitude acclimatization trend"
    )
    current_altitude: Optional[float] = Field(
        default=None, description="Current altitude"
    )
    previous_altitude: Optional[float] = Field(
        default=None, description="Previous altitude"
    )
    acclimatization_percentage: Optional[int] = Field(
        default=None, description="Overall acclimatization percentage"
    )
    previous_acclimatization_percentage: Optional[int] = Field(
        default=None, description="Previous overall acclimatization percentage"
    )
    altitude_acclimatization_local_timestamp: Optional[str] = Field(
        default=None, description="Local timestamp for altitude acclimatization"
    )


class TrainingStatusData(BaseModel):
    """Training status and load metrics"""

    training_status: Optional[str] = Field(
        default=None, description="Overall training status"
    )
    training_load_balance: Optional[str] = Field(
        default=None, description="Training load balance"
    )
    current_training_load: Optional[float] = Field(
        default=None, description="Current training load in minutes"
    )
    optimal_training_load: Optional[str] = Field(
        default=None, description="Optimal training load range"
    )
    acute_load: Optional[float] = Field(
        default=None, description="Acute training load in minutes (7 days)"
    )
    chronic_load: Optional[float] = Field(
        default=None, description="Chronic training load in minutes (28 days)"
    )
    training_stress_balance: Optional[float] = Field(
        default=None, description="Training stress balance"
    )

    # Monthly training load data
    monthly_load_aerobic_low: Optional[float] = Field(
        default=None, description="Monthly aerobic low training load in minutes"
    )
    monthly_load_aerobic_high: Optional[float] = Field(
        default=None, description="Monthly aerobic high training load in minutes"
    )
    monthly_load_anaerobic: Optional[float] = Field(
        default=None, description="Monthly anaerobic training load in minutes"
    )
    monthly_load_aerobic_low_target_min: Optional[int] = Field(
        default=None, description="Monthly aerobic low target minimum"
    )
    monthly_load_aerobic_low_target_max: Optional[int] = Field(
        default=None, description="Monthly aerobic low target maximum"
    )
    monthly_load_aerobic_high_target_min: Optional[int] = Field(
        default=None, description="Monthly aerobic high target minimum"
    )
    monthly_load_aerobic_high_target_max: Optional[int] = Field(
        default=None, description="Monthly aerobic high target maximum"
    )
    monthly_load_anaerobic_target_min: Optional[int] = Field(
        default=None, description="Monthly anaerobic target minimum"
    )
    monthly_load_anaerobic_target_max: Optional[int] = Field(
        default=None, description="Monthly anaerobic target maximum"
    )

    def __str__(self) -> str:
        """Human-readable summary of training status"""
        if not self.training_status:
            return "No training status data available"
        
        lines = [f"Training Status: {self.training_status}"]
        
        if self.training_load_balance:
            lines.append(f"Load Balance: {self.training_load_balance}")
        
        # Training loads
        # load_info = []
        # if self.acute_load is not None:
        #     load_info.append(f"Acute (7d): {self.acute_load:.1f}min")
        # if self.chronic_load is not None:
        #     load_info.append(f"Chronic (28d): {self.chronic_load:.1f}min")
        # if self.current_training_load is not None:
        #     load_info.append(f"Current: {self.current_training_load:.1f}min")
        
        # if load_info:
        #     lines.append(f"Training Load - {', '.join(load_info)}")
        
        # if self.training_stress_balance is not None:
        #     lines.append(f"Training Stress Balance: {self.training_stress_balance:.1f}")
        
        # if self.optimal_training_load:
        #     lines.append(f"Optimal Load Range: {self.optimal_training_load}")
        
        # Start with pipe-separated main info
        result = " | ".join(lines)
        
        # Add monthly loads and targets on new lines
        monthly_lines = []
        
        # Monthly loads
        monthly_loads = []
        if self.monthly_load_aerobic_low is not None:
            monthly_loads.append(f"Aerobic Low: {self.monthly_load_aerobic_low:.1f}min")
        if self.monthly_load_aerobic_high is not None:
            monthly_loads.append(f"Aerobic High: {self.monthly_load_aerobic_high:.1f}min")
        if self.monthly_load_anaerobic is not None:
            monthly_loads.append(f"Anaerobic: {self.monthly_load_anaerobic:.1f}min")
        
        if monthly_loads:
            monthly_lines.append(f"Monthly Loads: {', '.join(monthly_loads)}")
        
        # Monthly targets
        target_ranges = []
        if (self.monthly_load_aerobic_low_target_min is not None and 
            self.monthly_load_aerobic_low_target_max is not None):
            target_ranges.append(f"Aerobic Low: {self.monthly_load_aerobic_low_target_min}-{self.monthly_load_aerobic_low_target_max}min")
        if (self.monthly_load_aerobic_high_target_min is not None and 
            self.monthly_load_aerobic_high_target_max is not None):
            target_ranges.append(f"Aerobic High: {self.monthly_load_aerobic_high_target_min}-{self.monthly_load_aerobic_high_target_max}min")
        if (self.monthly_load_anaerobic_target_min is not None and 
            self.monthly_load_anaerobic_target_max is not None):
            target_ranges.append(f"Anaerobic: {self.monthly_load_anaerobic_target_min}-{self.monthly_load_anaerobic_target_max}min")
        
        if target_ranges:
            monthly_lines.append(f"Monthly Targets: {', '.join(target_ranges)}")
        
        if monthly_lines:
            result += "\n" + "\n".join(monthly_lines)
        
        return result


class GoalsData(BaseModel):
    """Active goals and targets"""

    active_goals: List[Goal] = Field(
        default_factory=list, description="List of active goals"
    )
    upcoming_events: List[str] = Field(
        default_factory=list, description="Upcoming race events"
    )
    goal_progress_summary: Optional[str] = Field(
        default=None, description="Summary of goal progress"
    )


class RecentActivitiesData(BaseModel):
    """Recent activity summaries"""

    activities: List[ActivitySummary] = Field(
        default_factory=list, description="Recent activity summaries"
    )
    weekly_summary: Optional[Dict[str, Any]] = Field(
        default=None, description="Weekly activity summary"
    )
    activity_trends: Optional[Dict[str, Any]] = Field(
        default=None, description="Activity trend analysis"
    )


class UserFitnessData(BaseModel):
    """Comprehensive user fitness data for training plan generation"""

    # Timestamp of data aggregation
    generated_at: str = Field(description="Timestamp when this data was generated")

    # User profile information
    user_profile: UserProfile = Field(description="User profile and settings")

    # Individual metric components
    body_battery: BodyBatteryData = Field(
        default_factory=BodyBatteryData, description="Body battery metrics"
    )
    sleep: SleepData = Field(
        default_factory=SleepData, description="Sleep quality and duration metrics"
    )
    heart_rate: HeartRateData = Field(
        default_factory=HeartRateData, description="Heart rate and HRV metrics"
    )
    stress: StressData = Field(
        default_factory=StressData, description="Stress and recovery indicators"
    )
    training_readiness: TrainingReadinessData = Field(
        default_factory=TrainingReadinessData,
        description="Training readiness assessment",
    )
    endurance: EnduranceData = Field(
        default_factory=EnduranceData, description="Endurance and aerobic fitness"
    )
    race_predictions: RacePredictionData = Field(
        default_factory=RacePredictionData, description="Race time predictions"
    )
    max_metrics: MaxMetricsData = Field(
        default_factory=MaxMetricsData,
        description="Max metrics including VO2 Max and environmental acclimatization",
    )
    training_status: TrainingStatusData = Field(
        default_factory=TrainingStatusData, description="Training status and load"
    )
    goals: GoalsData = Field(
        default_factory=GoalsData, description="Active goals and targets"
    )
    recent_activities: RecentActivitiesData = Field(
        default_factory=RecentActivitiesData, description="Recent activity data"
    )

    # Training availability and preferences
    training_availability: Optional[TrainingAvailability] = Field(
        default=None, description="Training schedule and availability"
    )

    # Additional context for training plan generation
    notes: Optional[str] = Field(
        default=None, description="Additional notes or context for training planning"
    )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response"""
        return {
            "generatedAt": self.generated_at,
            "userProfile": self.user_profile.model_dump(),
            "bodyBattery": self.body_battery.model_dump(),
            "sleep": self.sleep.model_dump(),
            "heartRate": self.heart_rate.model_dump(),
            "stress": self.stress.model_dump(),
            "trainingReadiness": self.training_readiness.model_dump(),
            "endurance": self.endurance.model_dump(),
            "racePredictions": self.race_predictions.model_dump(),
            "maxMetrics": self.max_metrics.model_dump(),
            "trainingStatus": self.training_status.model_dump(),
            "goals": self.goals.model_dump(),
            "recentActivities": self.recent_activities.model_dump(),
            "trainingAvailability": (
                self.training_availability.model_dump()
                if self.training_availability
                else None
            ),
            "notes": self.notes,
        }

    def __str__(self) -> str:
        """Human-readable summary of fitness data"""
        lines = [
            f"User Fitness Data (Generated: {self.generated_at})",
            f"",
            f"Profile: {self.user_profile.user_data.gender.value}, Age ~{datetime.now().year - int(self.user_profile.user_data.birth_date[:4])}",
            f"Measurement System: {self.user_profile.user_data.measurement_system.value}",
            f"",
            f"Current Fitness:",
        ]

        if self.max_metrics.vo2_max_value:
            lines.append(f"  VO2 Max Running: {self.max_metrics.vo2_max_value}")
        if self.training_status.training_status:
            lines.append(f"  Training Status: {self.training_status}")
        
        # Add race predictions
        race_times = []
        if self.race_predictions.time_5k_seconds:
            minutes, seconds = divmod(self.race_predictions.time_5k_seconds, 60)
            race_times.append(f"5K: {minutes}:{seconds:02d}")
        if self.race_predictions.time_10k_seconds:
            minutes, seconds = divmod(self.race_predictions.time_10k_seconds, 60)
            race_times.append(f"10K: {minutes}:{seconds:02d}")
        if self.race_predictions.time_half_marathon_seconds:
            hours, remainder = divmod(self.race_predictions.time_half_marathon_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            race_times.append(f"Half: {hours}:{minutes:02d}:{seconds:02d}")
        if self.race_predictions.time_marathon_seconds:
            hours, remainder = divmod(self.race_predictions.time_marathon_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            race_times.append(f"Marathon: {hours}:{minutes:02d}:{seconds:02d}")
        
        if race_times:
            lines.append("  Race Predictions:\n    " + '\n    '.join(race_times))

        lines.extend(
            [
                f"",
                f"Recovery Status:",
            ]
        )

        if self.body_battery.current_level:
            lines.append(f"  Body Battery: {self.body_battery.current_level}%")
        if self.heart_rate.resting_heart_rate:
            lines.append(f"  Resting HR: {self.heart_rate.resting_heart_rate} bpm")
        if self.sleep.total_sleep_hours:
            lines.append(f"  Last Sleep: {self.sleep.total_sleep_hours:.1f}h")

        lines.extend(
            [
                f"",
                f"Activities past month: {len(self.recent_activities.activities)} activities",
                f"Active Goals: {len(self.goals.active_goals)} goals",
                f"Training Days: {', '.join(self.training_availability.available_training_days) if self.training_availability else 'Not configured'}",
            ]
        )

        return "\n".join(lines)
