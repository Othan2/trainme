from typing import Dict, Any
from ..garmin.models.run_workout import RunWorkout


RETRIEVE_PROPOSED_WORKOUTS_TOOL = {
    "name": "retrieve_proposed_workouts",
    "description": 
        """
        Retrieve all previously created workouts. Returns a summary of all workouts
        that have been created in this session.
        """,
    "input_schema": {
        "type": "object",
        "properties": {},
        "required": []
    }
}

def handle_retrieve_workouts_tool(tool_use, stored_workouts: Dict[str, RunWorkout]) -> Dict[str, Any]:
    """Handle retrieve_workouts tool execution."""
    if not stored_workouts:
        content = "No workouts have been created yet."
    else:
        content = str(len(stored_workouts)) + " created total.\n\n" + "\n\n".join(str(workout) for workout in stored_workouts.values())
    
    return {
        "type": "tool_result",
        "tool_use_id": tool_use.id,
        "content": content
    }
