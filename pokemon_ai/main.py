import logging

import joblib
import typer

from pokemon_ai.learning.trainer import Trainer

app = typer.Typer()


@app.command()
def learn(episodes: int = 10000, model_path: str = "models/model.pkl", debug: bool = False):
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    trainer = Trainer(episodes=episodes)
    trainer.train()
    # joblib.dump(trainer.agent.model, model_path)


if __name__ == "__main__":
    app()
