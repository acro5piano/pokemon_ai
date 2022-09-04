from random import seed

import pokemon_ai.simulator.moves as m
import pokemon_ai.simulator.pokedex as p
from pokemon_ai.simulator.battle import ActionChangeTo, ActionSelectMove, Agent, Battle


class JustAttackAgent(Agent):
    def choose_action(self, opponent: Agent):
        player_pokemon = self.get_active_pokemon()
        return ActionSelectMove(player_pokemon.actual_moves[0])

    def choose_action_on_pokemon_dead(self, opponent: Agent):
        return self.get_available_pokemons()[0]


def test_battle():
    seed(42)
    agent1 = JustAttackAgent([p.Jolteon([m.Thunderbolt()])])
    agent2 = JustAttackAgent([p.Starmie([m.Surf()])])
    battle = Battle(agent1, agent2)

    while True:
        print(battle)
        battle.forward_step()
        winner = battle.get_winner()
        if winner is not None:
            print(winner)
            break

    assert winner == agent1
    raise NotImplementedError
