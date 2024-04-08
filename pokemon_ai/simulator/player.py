import random
from enum import Enum

from pokemon_ai.simulator.dex import Snorlax, Zapdos


class Action(Enum):
    CHANGE_TO_0 = 0
    CHANGE_TO_1 = 1
    CHANGE_TO_2 = 2  # Not used
    CHANGE_TO_3 = 3  # Not used
    CHANGE_TO_4 = 4  # Not used
    CHANGE_TO_5 = 5  # Not used
    MOVE_0 = 6
    MOVE_1 = 7
    MOVE_2 = 8  # Not used
    MOVE_3 = 9  # Not used

    def is_change(self) -> bool:
        return self.value < 6

    def is_move(self) -> bool:
        return self.value >= 6


class Player:
    pokemon1 = Zapdos
    pokemon2 = Snorlax

    def choose_action(self) -> Action:
        raise NotImplementedError


class RandomPlayer:
    pokemon1 = Zapdos
    pokemon2 = Snorlax

    def choose_action(self) -> Action:
        return random.choice([Action.CHANGE_TO_0, Action.CHANGE_TO_1, Action.MOVE_0, Action.MOVE_1])
