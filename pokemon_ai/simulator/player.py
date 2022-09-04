from __future__ import annotations

from dataclasses import dataclass
from typing import Union

from pokemon_ai.simulator.moves import Move
from pokemon_ai.simulator.pokedex import Pokemon


@dataclass
class ActionChangeTo:
    change_to: Pokemon

    def to_array(self):
        return [0, self.change_to.id]


@dataclass
class ActionSelectMove:
    move: Move

    def to_array(self):
        return [0, self.move.id]


Action = Union[ActionChangeTo, ActionSelectMove]


class Player:
    pokemons: list[Pokemon]
    active_pokemon_index = 0

    def __init__(self, pokemons: list[Pokemon]):
        self.pokemons = pokemons

    def choose_action(self, _opponent: Player) -> Action:
        raise NotImplementedError

    def choose_action_on_pokemon_dead(self, _opponent: Player) -> ActionChangeTo:
        raise NotImplementedError

    def change_pokemon_index_to(self, pokemon: Pokemon):
        self.active_pokemon_index = self.pokemons.index(pokemon)

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
        return [p.to_array() for p in self.pokemons]
