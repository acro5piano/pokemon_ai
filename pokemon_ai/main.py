import logging

import joblib
import typer

from pokemon_ai.dqn.value_function_agent import Trainer

app = typer.Typer()


@app.command()
def learn(episodes: int, debug: bool = False):
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    trainer = Trainer(episodes=episodes)
    trainer.train()
    joblib.dump(trainer.agent.model, "models/model.pkl")


@app.command()
def replay(episodes: int = 101, debug: bool = True):
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    model = joblib.load("models/model.pkl")
    trainer = Trainer(episodes=episodes, model=model)
    trainer.train()


@app.command()
def battle_with_sample(debug: bool = True):
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    trainer = Trainer(episodes=10)
    trainer.train()


if __name__ == "__main__":
    app()
