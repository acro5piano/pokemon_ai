from __future__ import annotations

from pokemon_ai.simulator.agent import Action, ActionChangeTo, ActionSelectMove, Agent


class JustAttackAgent(Agent):
    def choose_action(self, opponent: Agent) -> Action:
        player_pokemon = self.get_active_pokemon()
        return ActionSelectMove(player_pokemon.actual_moves[0])

    def choose_action_on_pokemon_dead(self, opponent: Agent) -> ActionChangeTo:
        return ActionChangeTo(self.get_available_pokemons()[0])


class JustChangeAgent(Agent):
    def choose_action(self, opponent: Agent) -> Action:
        available_pokemons = self.get_available_pokemons_for_change()
        if len(available_pokemons) == 0:
            return ActionSelectMove(self.get_active_pokemon().actual_moves[0])
        else:
            return ActionChangeTo(self.get_available_pokemons_for_change()[0])

    def choose_action_on_pokemon_dead(self, opponent: Agent) -> ActionChangeTo:
        return ActionChangeTo(self.get_available_pokemons()[0])
