from typing import Dict, Any, List
from ..garmin.client import Garmin


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

def handle_retrieve_garmin_workouts_tool(tool_use, garmin_client: Garmin):
    """Handle the retrieve_garmin_workouts tool call."""
    print(f"got tool_use:\n{tool_use}")
    inputs = tool_use.input if hasattr(tool_use, 'input') else {}
    
    start = inputs.get('start', 0)
    limit = inputs.get('limit', 100)
    
    try:
        workouts = garmin_client.get_workouts(start=start, end=limit)
        
        # Build detailed text response showing all workouts
        if not workouts:
            workout_text = "No workouts found in Garmin Connect."
        else:
            workout_lines = [f"Retrieved {len(workouts)} workouts from Garmin Connect:\n"]
            
            workout_lines.append("\n".join([str(workout) for workout in workouts]))
            
            workout_text = "\n\n".join(workout_lines)
        
        return {
            "tool_use_id": tool_use.id,
            "content": [{
                "type": "text",
                "text": workout_text
            }]
        }
        
    except Exception as e:
        return {
            "tool_use_id": tool_use.id,
            "content": [{
                "type": "text", 
                "text": f"Error retrieving workouts from Garmin Connect: {str(e)}"
            }]
        }
        
RETRIEVE_GARMIN_WORKOUT_DETAILS_TOOL = {
    "name": "retrieve_garmin_workout_details",
    "description": 
        """
        Retrieve detailed information about a specific workout from Garmin Connect.
        This fetches the full workout structure including segments, workout steps, and intensities.
        """,
    "input_schema": {
        "type": "object",
        "properties": {
            "workout_id": {
                "type": "integer",
                "description": "The ID of the workout to retrieve details for"
            }
        },
        "required": ["workout_id"]
    }
}


def handle_retrieve_garmin_workout_details_tool(tool_use, garmin_client: Garmin):
    """Handle the retrieve_garmin_workout_details tool call."""
    print(f"got tool_use:\n{tool_use}")
    inputs = tool_use.input if hasattr(tool_use, 'input') else {}
    
    workout_id = inputs.get('workout_id')
    if not workout_id:
        return {
            "tool_use_id": tool_use.id,
            "content": [{
                "type": "text",
                "text": "Error: workout_id is required"
            }]
        }
    
    try:
        workout_detail = garmin_client.get_workout_by_id(workout_id)
        return {
            "tool_use_id": tool_use.id,
            "content": [{
                "type": "text",
                "text": str(workout_detail) or "No workouts found."
            }]
        }
        
    except Exception as e:
        return {
            "tool_use_id": tool_use.id,
            "content": [{
                "type": "text", 
                "text": f"Error retrieving workout details from Garmin Connect: {str(e)}"
            }]
        }
