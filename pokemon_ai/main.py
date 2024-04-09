import logging

import joblib
import typer

from pokemon_ai.learning.trainer import Trainer
from pokemon_ai.simulator.battle import Battle
from pokemon_ai.simulator.player import RandomPlayer

app = typer.Typer()


@app.command()
def learn(episodes: int = 10000, model_path: str = "models/model.pkl", debug: bool = False):
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    trainer = Trainer(
        episodes=episodes, battle=Battle(player1=RandomPlayer(), player2=RandomPlayer())
    )
    trainer.train()
    # joblib.dump(trainer.agent.model, model_path)


if __name__ == "__main__":
    app()
