from typing import Dict, Any
from .models.workout import (
    SportType,
    EndConditionType,
    EndCondition,
    IntensityTarget,
    IntensityTargetType,
    NoTarget,
    CadenceTarget,
    HeartRateZoneTarget,
    PaceZoneTarget,
    StepType,
    WorkoutStep,
    WorkoutSegment,
    WorkoutOverview,
    Author,
    EstimatedDistanceUnit,
)
from .models.run_workout import RunWorkout


class WorkoutParser:
    """Parser to convert Garmin API workout JSON to RunWorkout objects"""

    @staticmethod
    def _parse_step_type(step_type_data: Dict[str, Any]) -> StepType:
        """Map JSON step type to StepType enum"""
        key = step_type_data.get("stepTypeKey")

        step_type_map = {
            "warmup": StepType.WARMUP,
            "cooldown": StepType.COOLDOWN,
            "interval": StepType.INTERVAL,
            "recovery": StepType.RECOVERY,
            "rest": StepType.REST,
            # "other": StepType.OTHER,
        }

        return step_type_map[key or "other"]

    @staticmethod
    def _parse_end_condition(step_data: Dict[str, Any]) -> EndCondition:
        """Parse JSON end condition to EndCondition object"""
        end_condition_data = step_data.get("endCondition", {})
        condition_key = end_condition_data.get("conditionTypeKey")
        value = step_data.get("endConditionValue", 0.0)
        displayable = end_condition_data.get("displayable", True)

        condition_map = {
            "lap.button": EndConditionType.LAP_BUTTON,
            "time": EndConditionType.TIME,
            "distance": EndConditionType.DISTANCE,
            "calories": EndConditionType.CALORIES,
        }

        condition_type = condition_map.get(condition_key, EndConditionType.LAP_BUTTON)
        return EndCondition(
            condition_type=condition_type, value=value, displayable=displayable
        )

    @staticmethod
    def _parse_intensity_target(step_data: Dict[str, Any]) -> IntensityTargetType:
        """Parse JSON target type to IntensityTarget object"""
        target_data = step_data.get("targetType", {})
        target_key = target_data.get("workoutTargetTypeKey")

        if target_key == "no.target":
            return NoTarget()
        elif target_key == "cadence":
            lower = step_data.get("targetValueOne")
            upper = step_data.get("targetValueTwo")
            if lower is not None and upper is not None:
                return CadenceTarget(lower_bound=lower, upper_bound=upper)
            return NoTarget()
        elif target_key == "heart.rate.zone":
            zone = step_data.get("zoneNumber")
            if zone is not None:
                return HeartRateZoneTarget(zone_number=zone)
            return NoTarget()
        elif target_key == "pace.zone":
            upper = step_data.get("targetValueOne")
            lower = step_data.get("targetValueTwo")
            if lower is not None and upper is not None:
                return PaceZoneTarget(lower_bound=lower, upper_bound=upper)
            return NoTarget()

        return NoTarget()

    @staticmethod
    def _parse_workout_step(step_data: Dict[str, Any]) -> WorkoutStep:
        """Parse JSON step data to WorkoutStep object"""
        step_order = step_data.get("stepOrder", 1)
        step_type = WorkoutParser._parse_step_type(step_data.get("stepType", {}))
        end_condition = WorkoutParser._parse_end_condition(step_data)
        intensity = WorkoutParser._parse_intensity_target(step_data)

        return WorkoutStep(
            step_order=step_order,
            step_type=step_type,
            end_condition=end_condition,
            intensity=intensity,
        )

    @staticmethod
    def _parse_workout_segment(segment_data: Dict[str, Any]) -> WorkoutSegment:
        """Parse JSON segment data to WorkoutSegment object"""
        segment_order = segment_data.get("segmentOrder", 1)
        sport_type = SportType.RUNNING  # Assuming running for now

        workout_steps = []
        for step_data in segment_data.get("workoutSteps", []):
            if step_data.get("type") == "ExecutableStepDTO":
                workout_step = WorkoutParser._parse_workout_step(step_data)
                workout_steps.append(workout_step)

        return WorkoutSegment(
            segment_order=segment_order,
            sport_type=sport_type,
            workout_steps=workout_steps,
        )

    @staticmethod
    def _parse_author(author_data: Dict[str, Any]) -> Author:
        """Parse JSON author data to Author object"""
        return Author(
            user_profile_pk=author_data.get("userProfilePk"),
            display_name=author_data.get("displayName"),
            full_name=author_data.get("fullName"),
            profile_img_name_large=author_data.get("profileImgNameLarge"),
            profile_img_name_medium=author_data.get("profileImgNameMedium"),
            profile_img_name_small=author_data.get("profileImgNameSmall"),
            user_pro=author_data.get("userPro", False),
            vivokid_user=author_data.get("vivokidUser", False),
        )

    @staticmethod
    def _parse_estimated_distance_unit(
        unit_data: Dict[str, Any],
    ) -> EstimatedDistanceUnit:
        """Parse JSON unit data to EstimatedDistanceUnit object"""
        return EstimatedDistanceUnit(unit_key=unit_data.get("unitKey"))

    # Parses a workout from
    @staticmethod
    def parse_workout(workout_json: Dict[str, Any]) -> RunWorkout:
        """Parse complete JSON workout to RunWorkout object"""
        workout_name = workout_json.get("workoutName", "Untitled Workout")
        training_plan_id = workout_json.get("trainingPlanId", None)

        workout_segments = []
        for segment_data in workout_json.get("workoutSegments", []):
            segment = WorkoutParser._parse_workout_segment(segment_data)
            workout_segments.append(segment)

        return RunWorkout(
            workout_name=workout_name,
            workout_segments=workout_segments,
            training_plan_id=training_plan_id,
            scheduled_date=None,
        )

    @staticmethod
    def parse_workout_overview(overview_json: Dict[str, Any]) -> WorkoutOverview:
        """Parse JSON workout overview to WorkoutOverview object"""
        sport_type = SportType.RUNNING  # Default to running for now

        author_data = overview_json.get("author", {})
        author = WorkoutParser._parse_author(author_data)

        estimated_distance_unit = None
        if overview_json.get("estimatedDistanceUnit"):
            estimated_distance_unit = WorkoutParser._parse_estimated_distance_unit(
                overview_json["estimatedDistanceUnit"]
            )

        pool_length_unit = None
        if overview_json.get("poolLengthUnit"):
            pool_length_unit = WorkoutParser._parse_estimated_distance_unit(
                overview_json["poolLengthUnit"]
            )

        return WorkoutOverview(
            workout_id=overview_json.get("workoutId", 0),
            owner_id=overview_json.get("ownerId", 0),
            workout_name=overview_json.get("workoutName", "Untitled Workout"),
            sport_type=sport_type,
            update_date=overview_json.get("updateDate", ""),
            created_date=overview_json.get("createdDate", ""),
            author=author,
            shared=overview_json.get("shared", False),
            estimated=overview_json.get("estimated", False),
            description=overview_json.get("description"),
            training_plan_id=overview_json.get("trainingPlanId"),
            estimated_duration_in_secs=overview_json.get("estimatedDurationInSeconds"),
            estimated_distance_in_meters=overview_json.get("estimatedDistanceInMeters"),
            estimate_type=overview_json.get("estimateType"),
            estimated_distance_unit=estimated_distance_unit,
            pool_length=overview_json.get("poolLength", 0.0),
            pool_length_unit=pool_length_unit,
            workout_provider=overview_json.get("workoutProvider"),
            workout_source_id=overview_json.get("workoutSourceId"),
            consumer=overview_json.get("consumer"),
            atp_plan_id=overview_json.get("atpPlanId"),
            workout_name_i18n_key=overview_json.get("workoutNameI18nKey"),
            description_i18n_key=overview_json.get("descriptionI18nKey"),
            workout_thumbnail_url=overview_json.get("workoutThumbnailUrl"),
        )
