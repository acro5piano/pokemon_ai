from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

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
    player1: Player
    player2: Player
    turn = 0

    def __init__(self, player1: Player, player2: Player):
        self.player1 = player1
        self.player2 = player2

    def forward_step(self):
        self.turn += 1
        action1 = self.player1.choose_action()
        action2 = self.player2.choose_action()
        pokemon1 = self.player1.active_pokemon()
        pokemon2 = self.player2.active_pokemon()
        if pokemon1.spe > pokemon2.spe:
            if action1 == Action.MOVE_1:
                damage1 = calculate_damage(pokemon1, pokemon2, pokemon1.get_move(1))
                pokemon2.hp -= damage1
            if action1 == Action.CHANGE_TO_1:
                self.player1.change_pokemon(1)
            if action1 == Action.CHANGE_TO_2:
                self.player1.change_pokemon(2)


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
