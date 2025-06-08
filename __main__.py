from src.garmin.client import Garmin
from src.garmin.models.run_workout import RunWorkout
from src.garmin.models.workout import (
    WorkoutSegment, WorkoutStep, SportType, StepType, 
    EndCondition, EndConditionType, NoTarget, PaceZoneTarget
)
from src.claude.client import Claude
from getpass import getpass

def main():
    email = input("Enter Garmin username: ")
    password = getpass("Enter Garmin password: ")
    
    
    
    with Garmin(email=email, password=password, return_on_mfa=True) as client:
        print('h')

if __name__ == "__main__":
    main()
