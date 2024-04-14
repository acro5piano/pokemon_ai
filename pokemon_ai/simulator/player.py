import random
from enum import Enum
from typing import Literal

from pokemon_ai.simulator.dex import Pokemon, Snorlax, Zapdos


class Action(Enum):
    MOVE_0 = 0
    MOVE_1 = 1
    # MOVE_2 = 7
    # MOVE_3 = 8
    # CHANGE_TO_0 = 0
    # CHANGE_TO_1 = 1
    # CHANGE_TO_2 = 2
    # CHANGE_TO_3 = 3
    # CHANGE_TO_4 = 4
    # CHANGE_TO_5 = 5

    def is_change(self) -> bool:
        return self.value < 5

    def is_move(self) -> bool:
        return self.value >= 5

    def to_move(self):
        return self.value - 4


PokemonIndex = Literal[0, 1]
# PokemonIndex = Literal[0, 1, 2, 3, 4, 5]


class Player:
    pokemon0: Pokemon
    pokemon1: Pokemon
    active_pokemon_index: PokemonIndex = 0

    def choose_action(self) -> Action:
        raise NotImplementedError

    def active_pokemon(self) -> Pokemon:
        match self.active_pokemon_index:
            case 0:
                return self.pokemon0
            case 1:
                return self.pokemon1

    def change_pokemon(self, index: PokemonIndex):
        self.active_pokemon_index = index


class RandomPlayer(Player):
    def __init__(self):
        self.pokemon0 = Snorlax()

    def choose_action(self) -> Action:
        return random.choice(
            [
                Action.MOVE_0,
                Action.MOVE_1,
            ]
        )
