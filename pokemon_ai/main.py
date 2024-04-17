import logging
import random

# import joblib
import typer

from pokemon_ai.learning.environment import Environment
from pokemon_ai.learning.monte_carlo_agent import MonteCarloAgent
from pokemon_ai.learning.players import RandomPlayer
from pokemon_ai.simulator.dex import Snorlax

random.seed(42)

app = typer.Typer()


@app.command()
def learn(
    episodes: int = 100000,
    play: bool = False,
    # model_path: str = "models/model.pkl",
    debug: bool = False,
):
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    env = Environment(RandomPlayer([Snorlax()]))
    agent = MonteCarloAgent(epsilon=0.1)
    agent.learn(env, episodes=episodes)
    if play:
        agent.play(env)
    # joblib.dump(trainer.agent.model, model_path)


if __name__ == "__main__":
    app()
