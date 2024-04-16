import random
from enum import Enum
from typing import Literal

from pokemon_ai.environment.simulator.dex import Pokemon, Snorlax, Zapdos


class Action(Enum):
    MOVE_0 = 0
    MOVE_1 = 1
    # MOVE_2 = 2
    # MOVE_3 = 3
    CHANGE_TO_0 = 4
    CHANGE_TO_1 = 5
    # CHANGE_TO_2 = 6
    # CHANGE_TO_3 = 7
    # CHANGE_TO_4 = 8
    # CHANGE_TO_5 = 9

    def is_move(self) -> bool:
        return self.value <= 3

    def is_change(self) -> bool:
        return self.value > 3

    def to_change_to_index(self):
        return self.value - 3


PokemonIndex = Literal[0, 1]
# PokemonIndex = Literal[0, 1, 2, 3, 4, 5]


class Player:
    pokemons: list[Pokemon]
    active_pokemon_index: PokemonIndex = 0

    def choose_action(self) -> Action:
        raise NotImplementedError

    def active_pokemon(self) -> Pokemon:
        return self.pokemons[self.active_pokemon_index]

    def change_pokemon(self, index: PokemonIndex):
        self.active_pokemon_index = index


class RandomPlayer(Player):
    def __init__(self):
        self.pokemons = [Snorlax()]

    def choose_action(self) -> Action:
        return random.choice(
            [
                Action.MOVE_0,
                Action.MOVE_1,
            ]
        )
