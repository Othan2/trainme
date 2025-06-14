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


def retrieve_all_workouts(workouts: Dict[str, RunWorkout]) -> str:
    """Convert all workouts to a string representation."""
    if not workouts:
        return "No workouts have been created yet."
    
    return str(len(workouts)) + " created total.\n\n" + "\n\n".join(str(workout) for workout in workouts.values())


def handle_retrieve_workouts_tool(tool_use, stored_workouts: Dict[str, RunWorkout]) -> Dict[str, Any]:
    """Handle retrieve_workouts tool execution."""
    return {
        "type": "tool_result",
        "tool_use_id": tool_use.id,
        "content": retrieve_all_workouts(stored_workouts)
    }
