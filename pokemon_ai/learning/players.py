import random

from pokemon_ai.simulator.player import Action, Player


class RandomPlayer(Player):
    def choose_action(self) -> Action:
        return random.choice(self.possible_actions())
