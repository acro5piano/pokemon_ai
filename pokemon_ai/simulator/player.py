from typing import Literal

from pokemon_ai.simulator.action import Action
from pokemon_ai.simulator.dex import Pokemon

PokemonIndex = Literal[0]


class Player:
    active_pokemon_index: int
    pokemons: list[Pokemon]

    def __init__(self, pokemons: list[Pokemon]):
        self.pokemons = pokemons
        self.active_pokemon_index = 0

    def active_pokemon(self) -> Pokemon:
        return self.pokemons[self.active_pokemon_index]

    def change_pokemon(self, index: PokemonIndex):
        target_pokemon = self.pokemons[index]
        if target_pokemon.hp <= 0:
            raise Exception("Invalid Target Pokemon")
        self.active_pokemon_index = index

    def is_dead(self):
        return all(x.hp <= 0 for x in self.pokemons)

    def possible_actions(self) -> list[Action]:
        pa: list[Action] = [
            Action.MOVE_0,
            Action.MOVE_1,
        ]
        return pa

    def choose_action(self) -> Action:
        raise NotImplementedError
