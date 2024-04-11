from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Tuple

from numpy import array, ndarray

from pokemon_ai.simulator.dex import BodySlam, Move, Pokemon, Snorlax, Thunder, Zapdos
from pokemon_ai.simulator.player import Action, Player


class Battle:
    agent: Player
    opponent: Player
    turn = 0

    def __init__(self, opponent: Player):
        self.opponent = opponent

    def forward_step(self, agent_action: Action):
        self.turn += 1
        opponent_action = self.opponent.choose_action()
        # TODO: define them
        return

    # TODO: use np.array
    def to_array(self) -> ndarray:
        return array(
            [
                self.agent.active_pokemon_index,
                self.agent.pokemon0.hp,
                self.agent.pokemon1.hp,
                self.opponent.active_pokemon_index,
                self.opponent.pokemon0.hp,
                self.opponent.pokemon1.hp,
            ]
        )


# Simplified damage calculation
def calculate_damage(attacker: Pokemon, defender: Pokemon, move: Move):
    match [attacker, defender, move]:
        case [Zapdos(), Zapdos(), Thunder()]:
            return 178
        case [Zapdos(), Snorlax(), Thunder()]:
            return 156
        case [Snorlax(), Zapdos(), BodySlam()]:
            return 119
        case [Snorlax(), Snorlax(), BodySlam()]:
            return 138
        case _:
            raise NotImplementedError
