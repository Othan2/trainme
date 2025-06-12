from typing import Dict, Any, List


RETRIEVE_GARMIN_WORKOUTS_TOOL = {
    "name": "retrieve_garmin_workouts",
    "description": 
        """
        Retrieve workouts from Garmin Connect. This fetches workouts that exist
        in your Garmin Connect account.
        """,
    "input_schema": {
        "type": "object",
        "properties": {
            "start": {
                "type": "integer",
                "description": "Starting workout offset (default: 0)",
                "default": 0
            },
            "limit": {
                "type": "integer", 
                "description": "Number of workouts to return (default: 100)",
                "default": 100
            }
        },
        "required": []
    }
}

# WIP: need a way to convert json response from garmin into Workouts.
