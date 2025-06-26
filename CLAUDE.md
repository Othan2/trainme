# TrainMe - Running Training App

## Project Overview

This is a CLI app that creates an interactive session with Claude to generate
running workouts and imports them into Garmin Connect.

Keep code files short to limit model token usage.

## Working with Claude

### Commands to Run

- **Code formatting**: `npm run prettier`
- **Linting**: `black src/`
- **Markdown linting**: `markdownlint *.md`
- **Type checking**: `mypy src/`

### Testing

### Project Structure

- `src/garmin/` - Garmin Connect integration
- `src/mcp_server.py` - MCP server implementation
- Main functionality focuses on workout generation and Garmin import

### Development Notes

- ALWAYS run prettier, linting and type checking after making changes
- Keep functions and files concise
- Follow existing code patterns and conventions
- Check for existing libraries before adding new dependencies

### Key Files

- `src/garmin/client.py` - Garmin Connect client (modified)
- `src/mcp_server.py` - MCP server (modified)
- `src/garmin/models/user_fitness_data.py` - New fitness data models
