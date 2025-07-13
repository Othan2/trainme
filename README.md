# trainme (WIP)

Conversational running trainer that syncs back to garmin.

## quickstart

### setup

```shell
# requires python >= 3.10
uv sync

# setup env
cp .env.example .env

# add your information
vim .env
# or
nano .env
```

### Run

```shell
uv run python .
```

## TODOs

- Better feedback loop to claude to ensure it does what you ask (creates 5 week plan when not asked, not 3 week plan)
- Confirmation of plan and upload activities to Garmin
- Better plan generation - some of the workouts created do not look good
- Plan modification in response to feedback.
- Adding length to the plan should not create (many) new workouts - should be much the same as the rest of the plan
- Plan should be an actual week-by-week plan rather than a set of workouts.
- Pull as much info about user preferences as possible out of Garmin.get_user_profile

## Acknowledgements

- Ripped a lot of client code from <https://github.com/cyberjunky/python-garminconnect>
