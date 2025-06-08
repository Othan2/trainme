from src.garmin.client import Garmin
from src.garmin.models.run_workout import RunWorkout
from src.garmin.models.workout import (
    WorkoutSegment, WorkoutStep, SportType, StepType, 
    EndCondition, EndConditionType, NoTarget, PaceZoneTarget
)
from getpass import getpass

def main():
    email = input("Enter Garmin username: ")
    password = getpass("Enter Garmin password: ")
    
    with Garmin(email=email, password=password, return_on_mfa=True) as client:
        print("Connected to Garmin Connect")
        workouts = client.get_user_summary('2025-06-06')
        print(workouts)
        
        # Create workout steps
        warmup_step = WorkoutStep(
            step_order=1,
            step_type=StepType.WARMUP,
            end_condition=EndCondition(EndConditionType.TIME, 600.0),  # 10 minutes
            intensity=NoTarget()
        )
        
        main_step = WorkoutStep(
            step_order=2,
            step_type=StepType.INTERVAL,
            end_condition=EndCondition(EndConditionType.DISTANCE, 5000.0),  # 5km
            intensity=PaceZoneTarget(lower_bound=3.6, upper_bound=2.5)  # pace in meters per second
        )
        
        cooldown_step = WorkoutStep(
            step_order=3,
            step_type=StepType.COOLDOWN,
            end_condition=EndCondition(EndConditionType.TIME, 300.0),  # 5 minutes
            intensity=NoTarget()
        )
        
        # Create workout segment
        segment = WorkoutSegment(
            segment_order=1,
            sport_type=SportType.RUNNING,
            workout_steps=[warmup_step, main_step, cooldown_step]
        )
        
        # Create a new running workout
        new_workout = RunWorkout(
            workout_name="Easy 5K Run",
            workout_segments=[segment]
        )
        print(f"Created workout: {new_workout.workout_name}")
        print(f"Workout dict: {new_workout.to_dict()}")
        client.upload_workout(new_workout)

if __name__ == "__main__":
    main()
