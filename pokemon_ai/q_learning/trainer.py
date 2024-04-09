from pokemon_ai import logger
from pokemon_ai.simulator.battle import Battle


class Trainer:
    battle: Battle

    def __init__(self, episodes: int, battle: Battle) -> None:
        self.episodes = episodes
        self.battle = battle

    def train(self):
        logger.log(self.episodes)
        for step in range(0, self.episodes):
            if step % 100 == 0:
                print("step", step)
            self.battle.forward_step()
