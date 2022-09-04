from __future__ import annotations

from dataclasses import dataclass
from random import random
from typing import Optional, Union

from pokemon_ai.simulator.damage import calculate_damage
from pokemon_ai.simulator.moves import Move
from pokemon_ai.simulator.pokedex import Pokemon


@dataclass
class ActionChangeTo:
    change_to: Pokemon


@dataclass
class ActionSelectMove:
    move: Move


class Agent:
    pokemons: list[Pokemon]
    active_pokemon_index = 0

    def __init__(self, pokemons: list[Pokemon]):
        self.pokemons = pokemons

    def choose_action(self, _opponent: Agent) -> Union[ActionChangeTo, ActionSelectMove]:
        raise NotImplementedError

    def choose_action_on_pokemon_dead(self, _opponent: Agent) -> ActionChangeTo:
        raise NotImplementedError

    def change_pokemon_index_to(self, pokemon: Pokemon):
        self.active_pokemon_index = self.pokemons.index(pokemon)

    def get_active_pokemon(self) -> Pokemon:
        return self.pokemons[self.active_pokemon_index]

    def is_dead(self) -> bool:
        return len(self.get_available_pokemons()) == 0

    def get_available_pokemons(self) -> list[Pokemon]:
        return [p for p in self.pokemons if p.actual_hp > 0]

    def __repr__(self) -> str:
        return f"{self.__class__}({self.pokemons})"


class Battle:
    agent1: Agent
    agent2: Agent

    def __init__(self, agent1: Agent, agent2: Agent):
        self.agent1 = agent1
        self.agent2 = agent2

    def forward_step(self):
        if self.agent1.get_active_pokemon().actual_hp <= 0:
            action = self.agent1.choose_action_on_pokemon_dead(self.agent2)
            self.agent1.change_pokemon_index_to(action.change_to)
            return
        if self.agent2.get_active_pokemon().actual_hp <= 0:
            action = self.agent2.choose_action_on_pokemon_dead(self.agent1)
            self.agent2.change_pokemon_index_to(action.change_to)
            return

        action1 = self.agent1.choose_action(self.agent2)
        action2 = self.agent2.choose_action(self.agent1)

        if isinstance(action1, ActionChangeTo):
            self.agent1.change_pokemon_index_to(action1.change_to)
        if isinstance(action2, ActionChangeTo):
            self.agent2.change_pokemon_index_to(action2.change_to)

        active_pokemon1 = self.agent1.get_active_pokemon()
        active_pokemon2 = self.agent2.get_active_pokemon()

        if isinstance(action1, ActionSelectMove) and isinstance(action2, ActionSelectMove):
            c1, c2 = get_spe_ordered_pokemon(
                (active_pokemon1, action1.move), (active_pokemon2, action2.move)
            )
            c2[0].actual_hp -= calculate_damage(c1[0], c2[0], c1[1])
            if c2[0].actual_hp <= 0:
                c1[0].actual_hp -= calculate_damage(c2[0], c1[0], c2[1])
        else:
            if isinstance(action1, ActionSelectMove):
                active_pokemon2.actual_hp -= calculate_damage(
                    active_pokemon1, active_pokemon2, action1.move
                )
            if isinstance(action2, ActionSelectMove):
                active_pokemon1.actual_hp -= calculate_damage(
                    active_pokemon2, active_pokemon1, action2.move
                )

    def get_winner(self) -> Optional[Agent]:
        if self.agent1.is_dead():
            return self.agent2
        if self.agent2.is_dead():
            return self.agent1

    def __repr__(self) -> str:
        return f"Battle({self.agent1}, {self.agent2})"


PokemonMove = tuple[Pokemon, Move]


def get_spe_ordered_pokemon(c1: PokemonMove, c2: PokemonMove) -> tuple[PokemonMove, PokemonMove]:
    if c1[0].spe > c2[0].spe:
        return (c1, c2)
    if c1[0].spe < c2[0].spe:
        return (c2, c1)
    return (c1, c2) if random() > 0.5 else (c2, c1)
