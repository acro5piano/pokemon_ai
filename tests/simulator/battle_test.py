from random import seed

import pytest

import pokemon_ai.simulator.moves as m
import pokemon_ai.simulator.pokedex as p
from pokemon_ai.simulator.battle import Battle
from pokemon_ai.simulator.sample_players import JustAttackPlayer, JustChangePlayer


def test_battle_just_battle():
    seed(42)
    player1 = JustAttackPlayer([p.Jolteon([m.Thunderbolt()])])
    player2 = JustAttackPlayer([p.Starmie([m.Surf()])])
    battle = Battle(player1, player2)
    winner = battle.run()
    assert winner == player1


def test_battle_just_battle_2():
    seed(42)
    player1 = JustAttackPlayer([p.Rhydon([m.Earthquake()])])
    player2 = JustAttackPlayer([p.Starmie([m.Surf()])])
    battle = Battle(player1, player2)
    winner = battle.run()
    assert winner == player2


def test_battle_just_change():
    seed(42)
    player1 = JustChangePlayer([p.Rhydon([m.Earthquake()]), p.Jolteon([m.Thunderbolt()])])
    player2 = JustChangePlayer([p.Starmie([m.Earthquake()]), p.Jolteon([m.Thunderbolt()])])
    battle = Battle(player1, player2)
    with pytest.raises(Exception):
        battle.run()


def test_battle_just_battle_and_change():
    seed(42)
    player1 = JustChangePlayer([p.Rhydon([m.Earthquake()]), p.Jolteon([m.Thunderbolt()])])
    player2 = JustAttackPlayer([p.Starmie([m.Surf()]), p.Jolteon([m.Thunderbolt()])])
    battle = Battle(player1, player2)
    winner = battle.run()
    assert winner == player2
