# pokemon_ai

> [!NOTE]
> This project is archived. The implementation is kept as-is, together with a
> [failure analysis and reference experiment](docs/README.md) documenting what
> was learned.

Deep Q Network Pokemon AI

## Project knowledge

The archived reports cover why training stalled, how evaluation obscured the
result, and what worked in a smaller AI-generated self-play DQN experiment.
See **[docs/README.md](docs/README.md)** for the Japanese summary and original
visual reports. The AI-generated reference implementation is preserved under
**[reference/ai-generated-self-play-dqn](reference/ai-generated-self-play-dqn/)**.

# Setup

```
poetry install
```

# Run Unit Testing

```
poetry run python -m pytest tests/simulator/
```

# Training

```
poetry run python pokemon_ai/main.py learn
```

# Replay

```
poetry run python pokemon_ai/main.py replay
```
