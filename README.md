# pokemon_ai

[wip] Deep Q Network Pokemon AI, mainly for GSC OU

## Setup

```
poetry install
```

## Learn & Run

```
poetry run python pokemon_ai/main.py --episodes 100000 --play
```

## Unittest

```
poetry run pytest
```

# Implement plan

Basically, GSC OU rule is applied.

## Phase 1. Simple Q learning with over simplified environment

Environment:

- Do not consider
  - Critical hit
  - STAB
  - Team building
  - PP
  - Damage random value
  - Any other complex things
- Agent and opponent have the same pokemon:
  - Snorlax
    - Return
    - Earthquake
- Damage calculation
  - Return always 166 damage to the foe's Snorlax
  - Earthquake always 109 damage to the foe's Snorlax

Agents:

- The opponent picks an action randomly.
- Our agent should pick Return only, because it has more damage than Earthquake.
