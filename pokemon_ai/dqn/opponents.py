from random import random

from pokemon_ai.simulator.player import Action, Player


class JustAttackPlayer(Player):
    def choose_action(self, _opponent: Player) -> Action:
        return self.pick_random_move_action()

    def choose_action_on_pokemon_dead(self, _opponent: Player) -> Action:
        return Action.change_to(self.get_random_living_pokemon_index_to_replace())


class StupidRandomPlayer(Player):
    def choose_action(self, _opponent: Player) -> Action:
        available_pokemons = self.get_available_pokemons_for_change()
        if len(available_pokemons) == 0 or random() < 0.5:
            return self.pick_random_move_action()
        else:
            return Action.change_to(self.get_random_living_pokemon_index_to_replace())

    def choose_action_on_pokemon_dead(self, _opponent: Player) -> Action:
        return Action.change_to(self.get_random_living_pokemon_index_to_replace())
