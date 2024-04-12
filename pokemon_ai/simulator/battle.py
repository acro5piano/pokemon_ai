from __future__ import annotations

from dataclasses import dataclass
from random import random
from typing import List, Optional, Tuple

from numpy import array, ndarray

from pokemon_ai.simulator.dex import BodySlam, Move, Pokemon, Snorlax, Thunder, Zapdos
from pokemon_ai.simulator.player import Action, Player


class Battle:
    agent_player: Player
    opponent: Player
    turn: int

    def __init__(self, agent_player: Player, opponent: Player):
        self.agent_player = agent_player
        self.opponent = opponent
        self.turn = 0

    def forward_step(self, agent_action: Action):
        self.turn += 1
        opponent_action = self.opponent.choose_action()

        # For now, agent move first
        # TODO: randomize the spe
        if agent_action == Action.MOVE_0:
            self.opponent.pokemon0.hp -= 138
        if agent_action == Action.MOVE_1:
            self.opponent.pokemon0.hp -= 109
        if self.opponent.pokemon0.hp <= 0:
            # TODO: type this
            return "AGENT_WON"

        if opponent_action == Action.MOVE_0:
            self.agent_player.pokemon0.hp -= 138
        if opponent_action == Action.MOVE_1:
            self.agent_player.pokemon0.hp -= 109
        if self.agent_player.pokemon0.hp <= 0:
            # TODO: type this
            return "OPPONENT_WON"

        # TODO: define them
        return

    # TODO: use np.array
    def to_array(self) -> ndarray:
        return array(
            [
                self.agent_player.active_pokemon_index,
                self.agent_player.pokemon0.hp,
                self.opponent.active_pokemon_index,
                self.opponent.pokemon0.hp,
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
