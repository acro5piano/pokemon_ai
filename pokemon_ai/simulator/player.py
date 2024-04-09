import random
from enum import Enum
from typing import Literal

from pokemon_ai.simulator.dex import Pokemon, Snorlax, Zapdos


class Action(Enum):
    CHANGE_TO_1 = 0
    CHANGE_TO_2 = 1
    # CHANGE_TO_3 = 2
    # CHANGE_TO_4 = 3
    # CHANGE_TO_5 = 4
    # CHANGE_TO_6 = 5
    MOVE_1 = 6
    # MOVE_2 = 7
    # MOVE_3 = 8
    # MOVE_4 = 9

    def is_change(self) -> bool:
        return self.value < 6

    def is_move(self) -> bool:
        return self.value >= 6

    def to_move(self):
        return self.value - 5


PokemonIndex = Literal[1, 2]


class Player:
    pokemon1: Pokemon
    pokemon2: Pokemon
    active_pokemon_index: PokemonIndex = 1

    def choose_action(self) -> Action:
        raise NotImplementedError

    def active_pokemon(self) -> Pokemon:
        match self.active_pokemon_index:
            case 1:
                return self.pokemon1
            case 2:
                return self.pokemon2

    def change_pokemon(self, index: PokemonIndex):
        self.active_pokemon_index = index


class RandomPlayer(Player):
    pokemon1 = Zapdos()
    pokemon2 = Snorlax()

    def choose_action(self) -> Action:
        return random.choice(
            [
                Action.CHANGE_TO_1,
                Action.CHANGE_TO_2,
                Action.MOVE_1,
            ]
        )
