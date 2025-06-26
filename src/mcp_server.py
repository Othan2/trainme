from typing import Optional
from fastmcp import FastMCP
from functools import wraps
import os
import sys
from pathlib import Path
import garth
from datetime import datetime

from garmin.client import Garmin
from src.garmin.models.workout import WorkoutDetailType

mcp = FastMCP(
    name="Garmin Connect Server",
    instructions="""
                 This server provides an integration with Garmin Connect.
                 The primary intent is to allow users to have a conversation about their health and fitness.
                 Users may also compose training plans that can be uploaded to Garmin.
                 """,
    dependencies=["src.garmin.client", "garth"],
)

email = os.getenv("GARMIN_EMAIL")
password = os.getenv("GARMIN_PASSWORD")
assert email is not None, "Garmin email is required to use this server."
assert password is not None, "Garmin password is required to use this server."

# Try to read existing token from tokenstore
tokens = None
try:
    with open("tokenstore", "r") as f:
        tokens = f.read().strip()
except FileNotFoundError:
    pass

# Login (will use existing token if valid, or get new token if needed)
tokens = Garmin(email, password, tokens=tokens).login()

# Save token to tokenstore file
with open("tokenstore", "w") as f:
    f.write(tokens)


@mcp.resource(
    uri="data://activities/{activityType}",
    description="Get activities from Garmin Connect as a resource.",
    mime_type="application/json",  # Explicit MIME type
)
def get_activities(
    start: int = 0, limit: int = 10, activityType: Optional[str] = None
) -> list[dict]:
    return Garmin.get_instance().get_activities(
        start=start, limit=limit, activitytype=activityType
    )


@mcp.resource(
    uri="data://user_profile",
    description="Get the user profile from Garmin Connect containing personal metrics and settings.",
    mime_type="application/json",
)
def get_user_profile() -> dict:
    profile = Garmin.get_instance().get_user_profile()
    return profile.model_dump()


@mcp.resource(
    uri="data://user_fitness_data",
    description="Get comprehensive user fitness data including profile, recent activities, fitness metrics, recovery data, and training goals - optimized for training plan generation.",
    mime_type="application/json",
)
def get_user_fitness_data(limit_activities: int = 15) -> dict:
    """
    Retrieve comprehensive fitness data that consolidates all user information
    needed for training plan generation in a single API call.

    This resource aggregates data from multiple Garmin Connect endpoints including:
    - User profile and preferences
    - Recent activity history with key metrics
    - Current fitness metrics (VO2 max, lactate threshold, etc.)
    - Recovery metrics (body battery, sleep, HRV, stress)
    - Training load and status
    - Active goals and objectives
    - Training availability and preferences

    Args:
        limit_activities: Number of recent activities to include (default: 15)

    Returns:
        dict: Comprehensive fitness data in unified format
    """
    try:
        garmin_client = Garmin.get_instance()
        fitness_data = garmin_client.get_comprehensive_fitness_data(
            limit_activities=limit_activities
        )
        return fitness_data.to_dict()
    except Exception as e:
        # Return error information in a structured format
        return {
            "error": "Failed to retrieve comprehensive fitness data",
            "details": str(e),
            "generatedAt": datetime.now().isoformat(),
            "userProfile": None,
            "fitnessMetrics": None,
            "trainingLoad": None,
            "recoveryMetrics": None,
            "recentActivities": [],
            "activeGoals": [],
            "trainingAvailability": None,
            "notes": f"Error occurred during data aggregation: {str(e)}",
        }


@mcp.tool
def create_workout(w: WorkoutDetailType) -> str:
    try:
        garmin_client = Garmin.get_instance()
        response = garmin_client.upload_workout(w)
        return f"Workout '{w.workout_name}' uploaded successfully to Garmin Connect. Response: {response.status_code}"
    except Exception as e:
        return (
            f"Failed to upload workout '{w.workout_name}' to Garmin Connect: {str(e)}"
        )


if __name__ == "__main__":
    mcp.run()
