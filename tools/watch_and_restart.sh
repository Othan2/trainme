#!/usr/bin/env zsh
# watch_and_restart.sh

# add the following to /Users/owenboyd/Library/Application Support/Claude/claude_desktop_config.json
# "mcp_server": {
#   "command": "/Users/owenboyd/projects/trainme/tools/watch_and_restart.sh"
# }

# Store the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${(%):-%x}")" && pwd)"

# Check if .env file exists
if [ ! -f "$SCRIPT_DIR/.env" ]; then
    echo "Error: .env file not found in script dir: $SCRIPT_DIR" >&2
    exit 1
fi

# Kill any existing server
pkill -f "fastmcp run"

source $SCRIPT_DIR/.env

# Function to start server
start_server() {
    cd $SCRIPT_DIR && \
    GARMIN_EMAIL=$GARMIN_EMAIL GARMIN_PASSWORD=$GARMIN_PASSWORD \
    uv run fastmcp run ../src/mcp_server.py &
    SERVER_PID=$!
}

# Start initial server
start_server

# Watch for changes
fswatch -o ../src/ | while read f; do
    # Files changed, restarting server...
    kill $SERVER_PID 2>/dev/null
    sleep 1
    start_server
done