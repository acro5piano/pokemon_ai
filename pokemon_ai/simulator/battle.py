from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from pokemon_ai.simulator.player import Action, Player


@dataclass
class StepResult:
    battle: Battle
    player1_action: Optional[Action] = None
    player2_action: Optional[Action] = None
    player1_took_damage: int = 0
    player2_took_damage: int = 0


class Battle:
    player1: Player
    player2: Player
    turn = 0

    def __init__(self, player1: Player, player2: Player):
        self.player1 = player1
        self.player2 = player2

    def forward_step(self):
        self.turn += 1
