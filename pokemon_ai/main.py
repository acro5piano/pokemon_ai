import logging
import random

import joblib
import typer

from pokemon_ai.agents.monte_carlo_agent import MonteCarloAgent
from pokemon_ai.environment.environment import Environment
from pokemon_ai.environment.simulator.battle import Battle
from pokemon_ai.environment.simulator.dex import Snorlax, Zapdos
from pokemon_ai.environment.simulator.player import RandomPlayer

random.seed(42)

app = typer.Typer()


@app.command()
def learn(
    episodes: int = 100000,
    play: bool = False,
    model_path: str = "models/model.pkl",
    debug: bool = False,
):
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    env = Environment(RandomPlayer([Snorlax(), Zapdos()]), RandomPlayer([Snorlax(), Zapdos()]))
    agent = MonteCarloAgent(epsilon=0.1)
    agent.learn(env, episodes=episodes)
    if play:
        agent.play(env)
    # joblib.dump(trainer.agent.model, model_path)


if __name__ == "__main__":
    app()
