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

### Debugging

Logs for the MCP server started can be found under `/Users/owenboyd/Library/Logs/Claude/mcp-server-mcp_server.log`. Only look at the last 500 lines initially.

### Testing

For each code change made:

1. Ensure the MCP server starts
2. Ensure that there are no errors in MCP server logs

### Project Structure

- `src/garmin/` - Garmin Connect integration
- `src/mcp_server.py` - MCP server implementation
- Main functionality focuses on workout generation and Garmin import

### Development Notes

- ALWAYS run prettier, linting and type checking after making changes
- Keep functions and files concise
- Follow existing code patterns and conventions
- Check for existing libraries before adding new dependencies
- If I reject several commands in a row, or ask you to look at chat logs, ALWAYS
  read .claude/logs/index.md for information on our prior chats.

### Key Files

- `src/garmin/client.py` - Garmin Connect client (modified)
- `src/mcp_server.py` - MCP server (modified)
- `src/garmin/models/user_fitness_data.py` - New fitness data models
