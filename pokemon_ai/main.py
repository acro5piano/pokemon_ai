import argparse

import joblib

from pokemon_ai.dqn.value_function_agent import Trainer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--episodes", type=int, required=True)
    parser.add_argument("--debug", type=bool, required=False, default=False)
    args = parser.parse_args()
    trainer = Trainer(episodes=args.episodes)
    trainer.train()
    joblib.dump(trainer.agent.model, "models/model.pkl")


if __name__ == "__main__":
    main()
