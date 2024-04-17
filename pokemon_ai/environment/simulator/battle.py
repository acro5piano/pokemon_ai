from __future__ import annotations

from enum import Enum

from numpy import array, ndarray

from pokemon_ai.environment.simulator.dex import (
    BodySlam,
    Earthquake,
    HiddenPowerIce,
    Move,
    Pokemon,
    Snorlax,
    Thunder,
    Zapdos,
)
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

        if agent_action.is_change():
            self.agent_player.change_pokemon(agent_action.to_change_to_index())
            if self.agent_player.active_pokemon().hp <= 0:
                # banned move!
                return BattleResult.OPPONENT_WON
        if opponent_action.is_change():
            self.opponent.change_pokemon(opponent_action.to_change_to_index())

        # For now, agent move first
        # TODO: randomize the spe
        if agent_action.is_move():
            self.opponent.active_pokemon().hp -= self.calculate_damage(
                self.agent_player.active_pokemon(),
                self.opponent.active_pokemon(),
                self.agent_player.active_pokemon().moves[agent_action.value],
            )
            if self.opponent.is_dead():
                return BattleResult.AGENT_WON
            if self.opponent.active_pokemon().hp <= 0:
                self.opponent.change_pokemon(0 if self.opponent.active_pokemon_index == 1 else 1)

        if opponent_action.is_move():
            self.agent_player.active_pokemon().hp -= self.calculate_damage(
                self.opponent.active_pokemon(),
                self.agent_player.active_pokemon(),
                self.opponent.active_pokemon().moves[opponent_action.value],
            )
            if self.agent_player.is_dead():
                return BattleResult.OPPONENT_WON
            if self.agent_player.active_pokemon().hp <= 0:
                self.agent_player.change_pokemon(
                    0 if self.opponent.active_pokemon_index == 1 else 1
                )

        return None

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
