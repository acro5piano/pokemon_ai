from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple

from pokemon_ai.simulator.dex import BodySlam, Move, Pokemon, Snorlax, Thunder, Zapdos
from pokemon_ai.simulator.player import Action, Player


@dataclass
class StepResult:
    battle: Battle
    player1_action: Optional[Action] = None
    player2_action: Optional[Action] = None
    player1_took_damage: int = 0
    player2_took_damage: int = 0


class Battle:
    agent: Player
    opponent: Player
    turn = 0

    def __init__(self, opponent: Player):
        self.opponent = opponent

    def forward_step(self, agent_action: Action):
        self.turn += 1
        opponent_action = self.opponent.choose_action()

    def to_array(self) -> Tuple[int, int]:
        return (
            self.agent.pokemon1.hp,
            self.agent.pokemon1.hp,
            self.agent.pokemon2.hp,
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
