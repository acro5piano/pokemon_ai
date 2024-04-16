from __future__ import annotations

from enum import Enum
from typing import Literal

from numpy import array, ndarray

from pokemon_ai.environment.simulator.dex import BodySlam, Move, Pokemon, Snorlax, Thunder, Zapdos
from pokemon_ai.environment.simulator.player import Action, Player


class BattleResult(Enum):
    AGENT_WON = "AGENT_WON"
    OPPONENT_WON = "OPPONENT_WON"


class Battle:
    agent_player: Player
    opponent: Player
    turn: int

    def __init__(self, agent_player: Player, opponent: Player):
        self.agent_player = agent_player
        self.opponent = opponent
        self.turn = 0

    def forward_step(self, agent_action: Action) -> None | BattleResult:
        self.turn += 1
        opponent_action = self.opponent.choose_action()

        # For now, agent move first
        # TODO: randomize the spe
        # TODO: consider Zapdos
        if agent_action == Action.MOVE_0:
            self.opponent.active_pokemon().hp -= 138
        if agent_action == Action.MOVE_1:
            self.opponent.active_pokemon().hp -= 109
        if self.opponent.active_pokemon().hp <= 0:
            return BattleResult.AGENT_WON

        if opponent_action == Action.MOVE_0:
            self.agent_player.active_pokemon().hp -= 138
        if opponent_action == Action.MOVE_1:
            self.agent_player.active_pokemon().hp -= 109
        if self.agent_player.active_pokemon().hp <= 0:
            return BattleResult.OPPONENT_WON

    # TODO: use np.array
    def to_array(self) -> ndarray:
        return array(
            [
                self.agent_player.active_pokemon_index,
                self.agent_player.pokemons[0].hp,
                self.agent_player.pokemons[1].hp,
                self.opponent.active_pokemon_index,
                self.opponent.pokemons[0].hp,
                self.opponent.pokemons[1].hp,
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
