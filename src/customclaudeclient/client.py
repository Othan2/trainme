import anthropic
from anthropic.types import TextBlock
from typing import List, Dict, Any, cast
import json

from ..garmin.client import Garmin
from ..garmin.models.run_workout import RunWorkout
from .create_workout_tool import CREATE_WORKOUTS_TOOL, handle_create_workouts_tool
from .retrieve_proposed_workouts_tool import (
    RETRIEVE_PROPOSED_WORKOUTS_TOOL,
    handle_retrieve_workouts_tool,
)
from .retrieve_garmin_workouts_tool import (
    RETRIEVE_GARMIN_WORKOUTS_TOOL,
    handle_retrieve_garmin_workouts_tool,
    RETRIEVE_GARMIN_WORKOUT_DETAILS_TOOL,
    handle_retrieve_garmin_workout_details_tool,
)


class Claude:
    def __init__(self, api_key: str, garmin_client: Garmin):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.garmin_client = garmin_client
        self.conversation_history = []
        self.workouts: Dict[str, RunWorkout] = {}
        self.tool_handlers = {
            "create_workouts": lambda tool_use: handle_create_workouts_tool(
                tool_use, self.workouts
            ),
            "retrieve_proposed_workouts": lambda tool_use: handle_retrieve_workouts_tool(
                tool_use, self.workouts
            ),
            "retrieve_garmin_workouts": lambda tool_use: handle_retrieve_garmin_workouts_tool(
                tool_use, self.garmin_client
            ),
            "retrieve_garmin_workout_details": lambda tool_use: handle_retrieve_garmin_workout_details_tool(
                tool_use, self.garmin_client
            ),
        }

    def get_workouts(self) -> Dict[str, RunWorkout]:
        """Get all stored workouts."""
        return self.workouts.copy()

    def chat(self, message: str) -> tuple[str, List[RunWorkout] | None]:
        """Chat interface with Claude that can create workouts."""
        system_message = """
        Use the create_workouts tool to structure workouts rather than just describing them in text.
        You can create workouts in multiple responses if needed.
        If the user asks you to create a training plan, the user must specify number of runs per week and miles per week before you can use the create_workouts tool.
        
        IMPORTANT: All workout names must be unique. If you try to create a workout with a name that already exists, you will receive an error and must choose a different name.
        
        You must run the following bits:
        - Any time the user responds with "yeah sure" or any variant of it, you must respond with: "Did you say "Yeah, sure" or "Yes sir"". You can vary this response a little if the user again responds with yeah sure.
        """

        # Add user message to history
        self.conversation_history.append({"role": "user", "content": message})

        chat_response = ""

        while True:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=20000,
                system=system_message,
                tools=[CREATE_WORKOUTS_TOOL, RETRIEVE_PROPOSED_WORKOUTS_TOOL, RETRIEVE_GARMIN_WORKOUTS_TOOL, RETRIEVE_GARMIN_WORKOUT_DETAILS_TOOL],  # type: ignore
                messages=self.conversation_history,
            )

            print(f"Claude stop_reason: {response.stop_reason}")

            tool_uses = []

            # First pass: extract text and collect tool_uses
            for content in response.content:
                if hasattr(content, "type") and content.type == "text":
                    text_content = self._extract_text(content)
                    chat_response += text_content
                elif hasattr(content, "type") and content.type == "tool_use":
                    tool_uses.append(content)

            # Add Claude's response to history
            self.conversation_history.append(
                {"role": "assistant", "content": response.content}
            )

            # Second pass: process all tool_uses together
            if tool_uses:
                tool_results = []
                for tool_use in tool_uses:
                    if tool_use.name in self.tool_handlers:
                        result = self.tool_handlers[tool_use.name](tool_use)
                        tool_results.append(result)

                # Convert tool results to proper format for conversation history
                content_blocks = []
                for result in tool_results:
                    content_blocks.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": result["tool_use_id"],
                            "content": result["content"],
                        }
                    )
                self.conversation_history.append(
                    {"role": "user", "content": content_blocks}
                )

            # Continue if stop reason is tool_use, otherwise break.
            # Allows claude to generate a bunch of workouts at once.
            if response.stop_reason != "tool_use":
                break

        return chat_response, list(self.workouts.values())

    def _extract_text(self, content_block) -> str:
        """Extract text from content block."""
        if isinstance(content_block, TextBlock):
            return content_block.text
        return str(content_block)

    def _should_continue_conversation(self, response: str) -> bool:
        """Check if Claude's response indicates it wants to continue with more content."""
        continuation_indicators = [
            "I'll continue",
            "I'll finish",
            "Let me continue",
            "I'll provide",
            "Next,",
            "Week 1:",  # Start of multi-week plan
            "continuing with",
            "moving on to",
            "Part 2",
            "Part 3",
        ]

        # Check for incomplete workout plans (mentions week 1 but not later weeks)
        if (
            "Week 1" in response
            and "Week 2" not in response
            and "Week 3" not in response
        ):
            return True

        # Check for continuation phrases
        response_lower = response.lower()
        return any(
            indicator.lower() in response_lower for indicator in continuation_indicators
        )

    def chat_complete(self, message: str) -> tuple[str, List[RunWorkout] | None]:
        """Chat with auto-continuation until Claude finishes the complete response."""
        all_workouts = []
        full_response = ""

        current_input = message
        while True:
            response, workouts = self.chat(current_input)
            full_response += response + " "

            if workouts:
                all_workouts.extend(workouts)

            if self._should_continue_conversation(response):
                current_input = "continue"
            else:
                break

        # Return summary of workouts created instead of garbled conversation
        if all_workouts:
            summary = f"Created {len(all_workouts)} workouts:\n"
            for i, workout in enumerate(all_workouts, 1):
                summary += f"{i}. {workout.workout_name}\n"
            return summary.strip(), all_workouts
        else:
            return full_response.strip(), None
