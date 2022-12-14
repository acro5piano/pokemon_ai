from __future__ import annotations

import logging
from dataclasses import dataclass
from random import random
from typing import Optional

from pokemon_ai.simulator.damage import calculate_damage
from pokemon_ai.simulator.moves import Move
from pokemon_ai.simulator.player import Action, Player
from pokemon_ai.simulator.pokedex import Pokemon


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

    def forward_step(self) -> StepResult:
        self.turn += 1

        if self.player1.get_active_pokemon().actual_hp <= 0:
            action = self.player1.choose_action_on_pokemon_dead(self.player2)
            self.player1.validate_change(action.value)
            self.player1.active_pokemon_index = action.value
            return StepResult(self, player1_action=action)
        if self.player2.get_active_pokemon().actual_hp <= 0:
            action = self.player2.choose_action_on_pokemon_dead(self.player1)
            self.player2.validate_change(action.value)
            self.player2.active_pokemon_index = action.value
            return StepResult(self, player2_action=action)

        action1 = self.player1.choose_action(self.player2)
        action2 = self.player2.choose_action(self.player1)

        result = StepResult(self, player1_action=action1, player2_action=action2)

        # Handle pokemon change
        if action1.is_change():
            self.player1.validate_change(action1.value)
            self.player1.active_pokemon_index = action1.value
            logging.info(f"{self.player1} changed their pokemon")
        if action2.is_change():
            self.player2.validate_change(action2.value)
            self.player2.active_pokemon_index = action2.value
            logging.info(f"{self.player2} changed their pokemon")

        active_pokemon1 = self.player1.get_active_pokemon()
        active_pokemon2 = self.player2.get_active_pokemon()

        # Handle pokemon damage
        if action1.is_move() and action2.is_move():
            # to handle both player choose a move
            c1, c2 = get_spe_ordered_pokemon(
                (active_pokemon1, active_pokemon1.actual_moves[action1.value - 6], self.player1),
                (active_pokemon2, active_pokemon2.actual_moves[action2.value - 6], self.player2),
            )
            logging.info(f"{c1[2]}'s {c1[0]} used {c1[1]}!")
            damage = calculate_damage(c1[0], c2[0], c1[1])
            c2[0].actual_hp -= damage
            logging.info(f"{c2[2]}'s {c2[0]} got {damage}")
            if c1[2] == self.player1:
                result.player2_took_damage = damage
            if c1[2] == self.player2:
                result.player1_took_damage = damage
            if c2[0].actual_hp > 0:
                logging.info(f"{c2[2]}'s {c2[0]} used {c2[1]}!")
                damage = calculate_damage(c2[0], c1[0], c2[1])
                c1[0].actual_hp -= damage
                logging.info(f"{c1[2]}'s {c1[0]} got {damage}")
                if c2[2] == self.player1:
                    result.player2_took_damage = damage
                if c2[2] == self.player2:
                    result.player1_took_damage = damage
        else:
            if action1.is_move():
                move = active_pokemon1.actual_moves[action1.value - 6]
                logging.info(f"{self.player1}'s {active_pokemon1} used {move}!")
                damage = calculate_damage(active_pokemon1, active_pokemon2, move)
                active_pokemon2.actual_hp -= damage
                logging.info(f"{self.player2}'s {active_pokemon2} got {damage}")
                result.player2_took_damage = damage
            if action2.is_move():
                move = active_pokemon2.actual_moves[action2.value - 6]
                logging.info(f"{self.player2}'s {active_pokemon2} used {move}!")
                damage = calculate_damage(active_pokemon2, active_pokemon1, move)
                active_pokemon1.actual_hp -= damage
                logging.info(f"{self.player1}'s {active_pokemon1} got {damage}")
                result.player1_took_damage = damage

        return result

    def get_winner(self) -> Optional[Player]:
        if self.player1.is_dead():
            return self.player2
        if self.player2.is_dead():
            return self.player1

    def __repr__(self) -> str:
        return f"Battle:\n  {self.player1}\n  {self.player2})"

    def validate(self):
        for Player in (self.player1, self.player2):
            if len([p for p in Player.pokemons if len(p.actual_moves) == 0]) > 0:
                raise ValueError("Pokemon must have at least one move")

    def run(self) -> Player:
        logging.info(self)
        self.validate()
        while True:
            logging.info("")
            self.forward_step()
            winner = self.get_winner()
            if winner is not None:
                logging.info(f"{winner} won the battle!")
                return winner
            if self.turn > 500:
                raise Exception("Battle is too long")
            logging.info(self)

    def to_array(self) -> list[float]:
        return [*self.player1.to_array(), *self.player2.to_array()]


PokemonMove = tuple[Pokemon, Move, Player]


def get_spe_ordered_pokemon(c1: PokemonMove, c2: PokemonMove) -> tuple[PokemonMove, PokemonMove]:
    if c1[0].spe > c2[0].spe:
        return (c1, c2)
    if c1[0].spe < c2[0].spe:
        return (c2, c1)
    return (c1, c2) if random() > 0.5 else (c2, c1)
