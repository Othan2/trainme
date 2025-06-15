from typing import Optional
from fastmcp import FastMCP
from functools import wraps
import os
import sys
from pathlib import Path
import garth

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

@mcp.tool
def create_workout(w: WorkoutDetailType) -> str:
    return str(w)


if __name__ == "__main__":
    mcp.run()
