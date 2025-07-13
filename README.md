# Trainme

Create workout plans with Claude and upload them to Garmin. Requires Claude
desktop, and integrates directly.

## Quickstart

### Add your garmin info to .env

```shell
# requires python >= 3.11.5
uv sync

# setup env
cp .env.example tools/.env

# add your information
vim tools/.env
# or
nano tools/.env
```

### Tell claude how to start MCP server

Add the following to `/Users/owenboyd/Library/Application Support/Claude/claude_desktop_config.json`

(Replace the `command` path below with the path on your computer to `tools/watch_and_restart.sh`)

```json
{
  "mcpServers": {
    "garmin_mcp": {
      "command": "/Users/owenboyd/projects/trainme/tools/watch_and_restart.sh"
    }
  }
}
```

### Create a plan through Claude

Insert screenshot here.

You can clear out old workouts created by Claude by asking it to delete workouts
it created in the last hour.

## Acknowledgements

- Ripped a lot of client code from <https://github.com/cyberjunky/python-garminconnect>
