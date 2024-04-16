import random
from enum import Enum
from typing import Literal

from pokemon_ai.environment.simulator.dex import Pokemon, Snorlax, Zapdos

PokemonIndex = Literal[0, 1]
# PokemonIndex = Literal[0, 1, 2, 3, 4, 5]

# TODO: make this to 4
MOVE_LENGTH = 2


class Action(Enum):
    MOVE_0 = 0
    MOVE_1 = 1

    # TODO: change it later
    CHANGE_TO_0 = 2
    CHANGE_TO_1 = 3

    # MOVE_2 = 2
    # MOVE_3 = 3
    # CHANGE_TO_0 = 4
    # CHANGE_TO_1 = 5
    # CHANGE_TO_2 = 6
    # CHANGE_TO_3 = 7
    # CHANGE_TO_4 = 8
    # CHANGE_TO_5 = 9

    def is_move(self) -> bool:
        # TODO
        return self.value <= 1

    def is_change(self) -> bool:
        # TODO
        return self.value >= 2

    def to_change_to_index(self) -> PokemonIndex:
        index = self.value - 2
        match index:
            case 0:
                return 0
            case 1:
                return 1
            case _:
                raise Exception("out of index")


class Player:
    pokemons: list[Pokemon]
    active_pokemon_index: PokemonIndex = 0

    def choose_action(self) -> Action:
        raise NotImplementedError

    def active_pokemon(self) -> Pokemon:
        return self.pokemons[self.active_pokemon_index]

    def change_pokemon(self, index: PokemonIndex):
        self.active_pokemon_index = index

    def is_dead(self):
        return all(x.hp <= 0 for x in self.pokemons)


class RandomPlayer(Player):
    def __init__(self):
        self.pokemons = [Snorlax(), Zapdos()]

    def choose_action(self) -> Action:
        return random.choice(
            [
                Action.MOVE_0,
                Action.MOVE_1,
                Action.CHANGE_TO_0,
                Action.CHANGE_TO_1,
            ]
        )
