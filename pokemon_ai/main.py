import joblib
import typer

from pokemon_ai.dqn.value_function_agent import Trainer

app = typer.Typer()


@app.command()
def learn(episodes: int, debug: bool = False):
    trainer = Trainer(episodes=episodes)
    trainer.train()
    joblib.dump(trainer.agent.model, "models/model.pkl")


@app.command()
def replay(episodes: int = 101, debug: bool = False):
    model = joblib.load("models/model.pkl")
    trainer = Trainer(episodes=episodes, model=model)
    trainer.train()


if __name__ == "__main__":
    app()
