from random import seed

import pytest

import pokemon_ai.simulator.moves as m
import pokemon_ai.simulator.pokedex as p
from pokemon_ai.simulator.battle import Battle
from pokemon_ai.simulator.sample_agents import JustAttackAgent, JustChangeAgent


def test_battle_just_battle():
    seed(42)
    agent1 = JustAttackAgent([p.Jolteon([m.Thunderbolt()])])
    agent2 = JustAttackAgent([p.Starmie([m.Surf()])])
    battle = Battle(agent1, agent2)
    winner = battle.run()
    assert winner == agent1


def test_battle_just_battle_2():
    seed(42)
    agent1 = JustAttackAgent([p.Rhydon([m.Earthquake()])])
    agent2 = JustAttackAgent([p.Starmie([m.Surf()])])
    battle = Battle(agent1, agent2)
    winner = battle.run()
    assert winner == agent2


def test_battle_just_change():
    seed(42)
    agent1 = JustChangeAgent([p.Rhydon([m.Earthquake()]), p.Jolteon([m.Thunderbolt()])])
    agent2 = JustChangeAgent([p.Starmie([m.Earthquake()]), p.Jolteon([m.Thunderbolt()])])
    battle = Battle(agent1, agent2)
    with pytest.raises(Exception):
        battle.run()


def test_battle_just_battle_and_change():
    seed(42)
    agent1 = JustChangeAgent([p.Rhydon([m.Earthquake()]), p.Jolteon([m.Thunderbolt()])])
    agent2 = JustAttackAgent([p.Starmie([m.Surf()]), p.Jolteon([m.Thunderbolt()])])
    battle = Battle(agent1, agent2)
    winner = battle.run()
    assert winner == agent2
