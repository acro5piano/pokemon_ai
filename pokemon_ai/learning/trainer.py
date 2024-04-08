from pokemon_ai import logger


class Trainer:
    def __init__(self, episodes: int) -> None:
        self.episodes = episodes

    def train(self):
        logger.log(self.episodes)
