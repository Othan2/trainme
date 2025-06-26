# TrainMe - Running Training App

## Project Overview

This is a CLI app that creates an interactive session with Claude to generate
running workouts and imports them into Garmin Connect.

Keep code files short to limit model token usage.

## Working with Claude

### Commands to Run

- **Linting**: `black src/`
- **Markdown linting**: `markdownlint *.md`
- **Type checking**: `mypy src/`
- **Tests**: Check if there's a test framework in use before running tests

### Project Structure

- `src/garmin/` - Garmin Connect integration
- `src/mcp_server.py` - MCP server implementation
- Main functionality focuses on workout generation and Garmin import

### Development Notes

- Always run linting and type checking after making changes
- Keep functions and files concise
- Follow existing code patterns and conventions
- Check for existing libraries before adding new dependencies

### Key Files

- `src/garmin/client.py` - Garmin Connect client (modified)
- `src/mcp_server.py` - MCP server (modified)
- `src/garmin/models/user_fitness_data.py` - New fitness data models
