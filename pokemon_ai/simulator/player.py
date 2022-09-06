from __future__ import annotations

import itertools
from enum import Enum

from pokemon_ai.simulator.pokedex import Pokemon


class Action(Enum):
    CHANGE_TO_0 = 0
    CHANGE_TO_1 = 1
    CHANGE_TO_2 = 2
    CHANGE_TO_3 = 3
    CHANGE_TO_4 = 4
    CHANGE_TO_5 = 5
    MOVE_0 = 6
    MOVE_1 = 7
    MOVE_2 = 8
    MOVE_3 = 9

    def is_change(self) -> bool:
        return self.value < 6

    def is_move(self) -> bool:
        return self.value >= 6

    @classmethod
    def change_to(cls, index: int) -> Action:
        match index:
            case 0:
                return cls.CHANGE_TO_0
            case 1:
                return cls.CHANGE_TO_1
            case 2:
                return cls.CHANGE_TO_2
            case 3:
                return cls.CHANGE_TO_3
            case 4:
                return cls.CHANGE_TO_4
            case 5:
                return cls.CHANGE_TO_5
            case _:
                raise NotImplementedError

    @classmethod
    def choose_move(cls, index: int) -> Action:
        match index:
            case 0:
                return cls.MOVE_0
            case 1:
                return cls.MOVE_1
            case 2:
                return cls.MOVE_2
            case 3:
                return cls.MOVE_3
            case _:
                raise NotImplementedError


class Player:
    pokemons: list[Pokemon]
    active_pokemon_index = 0

    def __init__(self, pokemons: list[Pokemon]):
        self.pokemons = pokemons

    def choose_action(self, _opponent: Player) -> Action:
        raise NotImplementedError

    def choose_action_on_pokemon_dead(self, _opponent: Player) -> Action:
        raise NotImplementedError

    def get_active_pokemon(self) -> Pokemon:
        return self.pokemons[self.active_pokemon_index]

    def is_dead(self) -> bool:
        return len(self.get_available_pokemons()) == 0

    def get_available_pokemons(self) -> list[Pokemon]:
        return [p for p in self.pokemons if p.actual_hp > 0]

    def get_available_pokemons_for_change(self) -> list[Pokemon]:
        return [p for p in self.pokemons if p.actual_hp > 0 and p != self.get_active_pokemon()]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.pokemons} active:{self.active_pokemon_index})"

    def to_array(self):
        list2d = [p.to_array() for p in self.pokemons]
        return list(itertools.chain(*list2d))
