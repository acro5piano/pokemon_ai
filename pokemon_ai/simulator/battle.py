from __future__ import annotations

from enum import Enum

from numpy import array, ndarray

from pokemon_ai.simulator.dex import (
    BodySlam,
    Earthquake,
    HiddenPowerIce,
    Move,
    Pokemon,
    Snorlax,
    Thunder,
    Zapdos,
)
from pokemon_ai.simulator.player import Action, Player


class BattleResult(Enum):
    PLAYER1_WON = "PLAYER1_WON"
    PLAYER2_WON = "PLAYER2_WON"


class Battle:
    player1: Player
    player2: Player
    turn: int

    def __init__(self, player1: Player, player2: Player):
        self.player1 = player1
        self.player2 = player2
        self.turn = 0

    def forward_step(
        self,
        player1_action: Action,
        player2_action: Action,
    ) -> None | BattleResult:
        self.turn += 1

        # For now, player1 move first
        # TODO: consider spe
        if player1_action.is_move():
            self.player2.active_pokemon().hp -= self.calculate_damage(
                self.player1.active_pokemon(),
                self.player2.active_pokemon(),
                self.player1.active_pokemon().moves[player1_action.value],
            )
            if self.player2.is_dead():
                return BattleResult.PLAYER1_WON

        if player2_action.is_move():
            self.player1.active_pokemon().hp -= self.calculate_damage(
                self.player2.active_pokemon(),
                self.player1.active_pokemon(),
                self.player2.active_pokemon().moves[player2_action.value],
            )
            if self.player1.is_dead():
                return BattleResult.PLAYER2_WON

        return None

    # TODO: use np.array
    def to_array(self) -> ndarray:
        return array(
            [
                self.player1.active_pokemon_index,
                self.player1.pokemons[0].hp,
                self.player2.active_pokemon_index,
                self.player2.pokemons[0].hp,
            ]
        )

    # Simplified damage calculation
    def calculate_damage(self, attacker: Pokemon, defender: Pokemon, move: Move):
        match [attacker, defender, move]:
            case [Zapdos(), Zapdos(), Thunder()]:
                return 178
            case [Zapdos(), Snorlax(), Thunder()]:
                return 156
            case [Zapdos(), Zapdos(), HiddenPowerIce()]:
                return 140
            case [Zapdos(), Snorlax(), HiddenPowerIce()]:
                return 61
            case [Snorlax(), Zapdos(), BodySlam()]:
                return 119
            case [Snorlax(), Snorlax(), BodySlam()]:
                return 138
            case [Snorlax(), Zapdos(), Earthquake()]:
                return 0
            case [Snorlax(), Snorlax(), Earthquake()]:
                return 109
            case _:
                raise NotImplementedError
