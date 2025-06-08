# Prompt to generate running model

The JSON provided models a sample run workout to be sent to the Garmin Connect API.
Using the json, generate a model in the parent folder in the file run_workout.py that models the running workout
in python.

Workouts are composed of steps. Any combination of step type, condition type, and target type is valid.

targetValueOne represents the lower bound for the target value. targetValueTwo represents the upper bound.

If a value is set to zero or null or some other default, prefer not to attempt to set a real value for it in the
json representation derived from the model, and instead leave it set to the default value.
