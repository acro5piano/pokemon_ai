from __future__ import annotations

import itertools
from enum import Enum

from pokemon_ai.simulator.pokedex import Pokemon


# TODO: support all type of action
class Action(Enum):
    CHANGE = 0
    FIGHT = 1


class Player:
    pokemons: list[Pokemon]
    active_pokemon_index = 0

    def __init__(self, pokemons: list[Pokemon]):
        self.pokemons = pokemons

    def choose_action(self, _opponent: Player) -> Action:
        raise NotImplementedError

    def choose_action_on_pokemon_dead(self, _opponent: Player) -> Action:
        return Action.CHANGE
        # raise NotImplementedError

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
