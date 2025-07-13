#!/usr/bin/env zsh
# watch_and_restart.sh

# add the following to /Users/owenboyd/Library/Application Support/Claude/claude_desktop_config.json
# "mcp_server": {
#   "command": "/Users/owenboyd/projects/trainme/tools/watch_and_restart.sh"
# }

set -euo pipefail

# Store the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${(%):-%x}")" && pwd)"
PID_FILE="$SCRIPT_DIR/.server.pid"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >&2
}

cleanup() {
    log "Shutting down..."
    if [ -f "$PID_FILE" ]; then
        local pid=$(cat "$PID_FILE")
        if kill -0 "$pid" 2>/dev/null; then
            kill "$pid"
            wait "$pid" 2>/dev/null || true
        fi
        rm -f "$PID_FILE"
    fi
    pkill -f "fastmcp run" 2>/dev/null || true
    exit 0
}

# Set up signal handlers
trap cleanup INT TERM EXIT

# Check dependencies
for cmd in fswatch uv; do
    if ! command -v "$cmd" >/dev/null 2>&1; then
        log "Error: $cmd is not installed"
        exit 1
    fi
done

# Check if .env file exists
if [ ! -f "$SCRIPT_DIR/.env" ]; then
    log "Error: .env file not found in script dir: $SCRIPT_DIR"
    exit 1
fi

# Kill any existing server
pkill -f "fastmcp run" 2>/dev/null || true

source "$SCRIPT_DIR/.env"

# Function to wait for server to be ready
wait_for_server() {
    local max_wait=5
    local count=0
    while [ $count -lt $max_wait ]; do
        if [ -f "$PID_FILE" ]; then
            local pid=$(cat "$PID_FILE")
            if kill -0 "$pid" 2>/dev/null; then
                sleep 0.5
                return 0
            fi
        fi
        sleep 0.5
        count=$((count + 1))
    done
    return 1
}

# Function to start server
start_server() {
    if [ -f "$PID_FILE" ]; then
        local old_pid=$(cat "$PID_FILE")
        if kill -0 "$old_pid" 2>/dev/null; then
            kill "$old_pid"
            wait "$old_pid" 2>/dev/null || true
        fi
    fi
    
    log "Starting server..."
    cd "$SCRIPT_DIR"
    GARMIN_EMAIL="$GARMIN_EMAIL" GARMIN_PASSWORD="$GARMIN_PASSWORD" \
    uv run fastmcp run ../src/mcp_server.py &
    
    echo $! > "$PID_FILE"
    log "Server started with PID $!"
    
    # Wait for server to be ready before returning
    wait_for_server
}

# Start initial server
start_server

# Watch for changes with debouncing
log "Watching ../src/ for changes..."
fswatch -o ../src/ | while read f; do
    log "Files changed, restarting server in 2 seconds..."
    sleep 2  # Debounce rapid changes
    start_server
done