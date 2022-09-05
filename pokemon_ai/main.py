import logging

import joblib
import typer

from pokemon_ai.dqn.value_function_agent import Trainer

app = typer.Typer()


@app.command()
def learn(episodes: int = 10000, model_path: str = "models/model.pkl", debug: bool = False):
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    trainer = Trainer(episodes=episodes)
    trainer.train()
    joblib.dump(trainer.agent.model, model_path)


@app.command()
def replay(episodes: int = 101, model_path: str = "models/model.pkl", debug: bool = True):
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    model = joblib.load(model_path)
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
