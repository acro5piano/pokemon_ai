import logging

import joblib
import typer

from pokemon_ai.q_learning.agent import Agent
from pokemon_ai.q_learning.environment import Environment
from pokemon_ai.simulator.battle import Battle
from pokemon_ai.simulator.player import RandomPlayer

app = typer.Typer()


@app.command()
def learn(episodes: int = 100000, model_path: str = "models/model.pkl", debug: bool = False):
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    env = Environment()
    agent = Agent(epsilon=0.1)
    agent.learn(env, episodes=episodes)
    agent.play(env)
    # joblib.dump(trainer.agent.model, model_path)


if __name__ == "__main__":
    app()
