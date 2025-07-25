from fastmcp import FastMCP
import os

from garmin.client import Garmin
from garmin.models.workout import WorkoutDetailType

mcp: FastMCP = FastMCP(
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
    uri="data://activities",
    description="Get activities from Garmin Connect as a resource.",
    mime_type="application/json",
)
def activities() -> str:
    return str(
        Garmin.get_instance().get_activities(start=0, limit=10, activitytype="running")
    )


@mcp.resource(
    uri="data://user_profile",
    description="Get the user profile from Garmin Connect containing personal metrics and settings.",
    mime_type="application/json",
)
def user_profile() -> str:
    return str(Garmin.get_instance().get_user_profile())


@mcp.resource(
    uri="data://user_fitness_data",
    description="Get comprehensive user fitness data including profile, recent activities, fitness metrics, recovery data, and training goals - optimized for training plan generation.",
    mime_type="application/json",
)
def user_fitness_data() -> str:
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
        str: Comprehensive fitness data in unified format
    """
    return str(
        Garmin.get_instance().get_comprehensive_fitness_data(limit_activities=15)
    )


@mcp.tool
def create_workouts(workouts: list[WorkoutDetailType]) -> str:
    """
    Upload multiple workouts to Garmin Connect. Also schedules them in user calendar.
    Returns summary and workout IDs for successfully created workouts.
    ALWAYS choose interval step types for the main "running" step type.
    ALWAYS prefer heartrate zones over pace zones unless explicitly provided pace.
    ALWAYS base long run duration on user's easy run pace.
    """
    # Validate all workouts first
    for i, workout in enumerate(workouts):
        if not hasattr(workout, "scheduled_date") or workout.scheduled_date is None:
            return f"Error: Workout {i+1} ('{workout.workout_name}') is missing required scheduled_date field"

    garmin_client = Garmin.get_instance()
    results = []
    successful = 0
    failed = 0
    scheduled = 0

    for i, workout in enumerate(workouts):
        try:
            response = garmin_client.create_workout(workout)
            workout_id = response.json().get("workoutId")
            successful += 1

            if workout_id:
                garmin_client.schedule_workout(str(workout_id), workout)
                date_str = (
                    workout.scheduled_date.strftime("%Y-%m-%d")
                    if workout.scheduled_date
                    else "unscheduled"
                )
                results.append(
                    f"✓ '{workout.workout_name}' uploaded and scheduled for {date_str} (ID: {workout_id})"
                )
                scheduled += 1
            else:
                results.append(
                    f"✓ '{workout.workout_name}' uploaded successfully (no ID returned)"
                )

        except Exception as e:
            results.append(f"✗ '{workout.workout_name}' failed: {str(e)}")
            failed += 1

    summary = f"Uploaded {successful} of {len(workouts)} workouts successfully"
    if scheduled > 0:
        summary += f" ({scheduled} scheduled)"
    if failed > 0:
        summary += f" ({failed} failed)"

    return f"{summary}\n\n" + "\n".join(results)


@mcp.tool
def update_workouts(workouts: list[tuple[int, WorkoutDetailType]]) -> str:
    """
    Update multiple existing workouts in Garmin Connect.
    Takes a list of tuples where each tuple contains (workout_id, workout_detail).

    Args:
        workouts: List of tuples containing (workout_id, workout_detail) pairs

    Returns:
        Summary of update results
    """
    garmin_client = Garmin.get_instance()
    results = []
    successful = 0
    failed = 0

    for workout_id, workout in workouts:
        try:
            garmin_client.update_workout(str(workout_id), workout)
            successful += 1
            results.append(
                f"✓ Workout {workout_id} ('{workout.workout_name}') updated successfully"
            )
        except Exception as e:
            failed += 1
            results.append(
                f"✗ Workout {workout_id} ('{workout.workout_name}') failed: {str(e)}"
            )

    summary = f"Updated {successful} of {len(workouts)} workouts successfully"
    if failed > 0:
        summary += f" ({failed} failed)"

    return f"{summary}\n\n" + "\n".join(results)


@mcp.tool
def delete_recent_workouts(max_age_hours: float = 1.0) -> str:
    """Delete workouts that are less than the specified age in hours."""
    from datetime import datetime, timezone, timedelta

    def parse_workout_date(date_str: str) -> datetime:
        if date_str.endswith("Z"):
            date_str = date_str.replace("Z", "+00:00")
        elif "+" not in date_str and "-" not in date_str[-6:]:
            date_str += "+00:00"
        return datetime.fromisoformat(date_str)

    try:
        garmin_client = Garmin.get_instance()
        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=max_age_hours)

        workouts = garmin_client.get_workouts_by_source()
        recent_workouts = [
            w for w in workouts if parse_workout_date(w.update_date) > cutoff_time
        ]

        if not recent_workouts:
            return f"No workouts found that are less than {max_age_hours} hours old"

        results = []
        for workout in recent_workouts:
            try:
                garmin_client.delete_workout(str(workout.workout_id))
                results.append(f"✓ '{workout.workout_name}' deleted")
            except Exception as e:
                results.append(f"✗ '{workout.workout_name}' failed: {e}")

        successful = sum(1 for r in results if r.startswith("✓"))
        failed = len(results) - successful

        summary = f"Deleted {successful}/{len(recent_workouts)} recent workouts"
        if failed > 0:
            summary += f" ({failed} failed)"

        return f"{summary}\n\n" + "\n".join(results)

    except Exception as e:
        return f"Failed to delete recent workouts: {e}"


if __name__ == "__main__":
    mcp.run()
