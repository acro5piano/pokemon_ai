from __future__ import annotations

from random import random
from typing import Optional

from pokemon_ai.logger import log
from pokemon_ai.simulator.damage import calculate_damage
from pokemon_ai.simulator.moves import Move
from pokemon_ai.simulator.player import ActionChangeTo, ActionSelectMove, Player
from pokemon_ai.simulator.pokedex import Pokemon


class Battle:
    player1: Player
    player2: Player
    turn = 0

    def __init__(self, player1: Player, player2: Player):
        self.player1 = player1
        self.player2 = player2

    def forward_step(self):
        self.turn += 1

        if self.player1.get_active_pokemon().actual_hp <= 0:
            action = self.player1.choose_action_on_pokemon_dead(self.player2)
            self.player1.change_pokemon_index_to(action.change_to)
            log(f"{self.player1} changed to {action.change_to}")
            return
        if self.player2.get_active_pokemon().actual_hp <= 0:
            action = self.player2.choose_action_on_pokemon_dead(self.player1)
            self.player2.change_pokemon_index_to(action.change_to)
            log(f"{self.player2} changed to {action.change_to}")
            return

        action1 = self.player1.choose_action(self.player2)
        action2 = self.player2.choose_action(self.player1)

        # Handle pokemon change
        if isinstance(action1, ActionChangeTo):
            if action1.change_to not in self.player1.get_available_pokemons_for_change():
                raise Exception(
                    f"{self.player1} tried to change to {action1.change_to} but it's not available"
                )
            self.player1.change_pokemon_index_to(action1.change_to)
            log(f"{self.player1} changed to {action1.change_to}")
        if isinstance(action2, ActionChangeTo):
            if action2.change_to not in self.player2.get_available_pokemons_for_change():
                raise Exception(
                    f"{self.player2} tried to change to {action2.change_to} but it's not available"
                )
            self.player2.change_pokemon_index_to(action2.change_to)
            log(f"{self.player2} changed to {action2.change_to}")

        active_pokemon1 = self.player1.get_active_pokemon()
        active_pokemon2 = self.player2.get_active_pokemon()

        # Handle pokemon damage
        if isinstance(action1, ActionSelectMove) and isinstance(action2, ActionSelectMove):
            # to handle both player choose a move
            c1, c2 = get_spe_ordered_pokemon(
                (active_pokemon1, action1.move), (active_pokemon2, action2.move)
            )
            log(f"{c1[0]} used {action1.move}!")
            damage = calculate_damage(c1[0], c2[0], c1[1])
            c2[0].actual_hp -= damage
            log(f"{c2[0]} got {damage}")
            if c2[0].actual_hp > 0:
                log(f"{c2[0]} used {action2.move}!")
                damage = calculate_damage(c2[0], c1[0], c2[1])
                c1[0].actual_hp -= damage
                log(f"{c1[0]} got {damage}")
        else:
            if isinstance(action1, ActionSelectMove):
                log(f"{active_pokemon1} used {action1.move}!")
                damage = calculate_damage(active_pokemon1, active_pokemon2, action1.move)
                active_pokemon2.actual_hp -= damage
                log(f"{active_pokemon2} got {damage}")
            if isinstance(action2, ActionSelectMove):
                log(f"{active_pokemon2} used {action2.move}!")
                damage = calculate_damage(active_pokemon2, active_pokemon1, action2.move)
                active_pokemon1.actual_hp -= damage
                log(f"{active_pokemon1} got {damage}")

    def get_winner(self) -> Optional[Player]:
        if self.player1.is_dead():
            return self.player2
        if self.player2.is_dead():
            return self.player1

    def __repr__(self) -> str:
        return f"Battle({self.player1}, {self.player2})"

    def validate(self):
        for Player in (self.player1, self.player2):
            if len([p for p in Player.pokemons if len(p.actual_moves) == 0]) > 0:
                raise ValueError("Pokemon must have at least one move")

    def run(self) -> Player:
        log(self)
        self.validate()
        while True:
            log("")
            self.forward_step()
            winner = self.get_winner()
            if winner is not None:
                log(f"{winner} won the battle!")
                return winner
            if self.turn > 500:
                raise Exception("Battle is too long")
            log(self)


PokemonMove = tuple[Pokemon, Move]


def get_spe_ordered_pokemon(c1: PokemonMove, c2: PokemonMove) -> tuple[PokemonMove, PokemonMove]:
    if c1[0].spe > c2[0].spe:
        return (c1, c2)
    if c1[0].spe < c2[0].spe:
        return (c2, c1)
    return (c1, c2) if random() > 0.5 else (c2, c1)
