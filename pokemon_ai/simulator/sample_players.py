from __future__ import annotations

from random import random

from pokemon_ai.simulator.player import Action, ActionChangeTo, ActionSelectMove, Player


class JustAttackPlayer(Player):
    def choose_action(self, opponent: Player) -> Action:
        player_pokemon = self.get_active_pokemon()
        return ActionSelectMove(player_pokemon.actual_moves[0])

    def choose_action_on_pokemon_dead(self, opponent: Player) -> ActionChangeTo:
        return ActionChangeTo(self.get_available_pokemons()[0])


class JustChangePlayer(Player):
    def choose_action(self, opponent: Player) -> Action:
        available_pokemons = self.get_available_pokemons_for_change()
        if len(available_pokemons) == 0:
            return ActionSelectMove(self.get_active_pokemon().actual_moves[0])
        else:
            return ActionChangeTo(self.get_available_pokemons_for_change()[0])

    def choose_action_on_pokemon_dead(self, opponent: Player) -> ActionChangeTo:
        return ActionChangeTo(self.get_available_pokemons()[0])


class StupidRandomPlayer(Player):
    def choose_action(self, opponent: Player) -> Action:
        available_pokemons = self.get_available_pokemons_for_change()
        if len(available_pokemons) == 0:
            return ActionSelectMove(self.get_active_pokemon().actual_moves[0])
        if random() < 0.5:
            return ActionSelectMove(self.get_active_pokemon().actual_moves[0])
        else:
            return ActionChangeTo(available_pokemons[0])

    def choose_action_on_pokemon_dead(self, opponent: Player) -> ActionChangeTo:
        # TODO: support pokemon num > 2
        # available_pokemons = self.get_available_pokemons()
        return ActionChangeTo(self.get_available_pokemons()[0])
