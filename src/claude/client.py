import anthropic
from anthropic.types import TextBlock


class Claude:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
    
    def generate_workout(self, prompt: str) -> str:
        """Generate a workout based on the given prompt."""
        message = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return self._extract_text(message.content[0])
    
    def chat(self, message: str) -> str:
        """Simple chat interface with Claude."""
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            messages=[
                {"role": "user", "content": message}
            ]
        )
        return self._extract_text(response.content[0])
    
    def _extract_text(self, content_block) -> str:
        """Extract text from content block."""
        if isinstance(content_block, TextBlock):
            return content_block.text
        return str(content_block)
