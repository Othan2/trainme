# trainme (WIP)

Conversational running trainer that syncs back to garmin.

## quickstart

### setup

```shell
# requirespython >= 3.11.5
pip install -r requirements.txt

# setup env
cp .env.example .env

# add your information
vim .env
# or
nano .env
```

### Run

```shell
python3 .
```

## TODOs

- Better feedback loop to claude to ensure it does what you ask (creates 5 week plan when not asked, not 3 week plan)
- Confirmation of plan and upload activities to Garmin
- Better plan generation - some of the workouts created do not look good
