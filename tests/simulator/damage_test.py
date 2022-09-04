from random import seed

from pokemon_ai.simulator.damage import calculate_damage, to_real_value
from pokemon_ai.simulator.moves import Earthquake, Thunderbolt
from pokemon_ai.simulator.pokedex import Jolteon, Rhydon, Starmie


def test_to_real_value():
    assert to_real_value(60) == 218
    assert to_real_value(130) == 358


def test_calculate_damage():
    seed(42)
    assert calculate_damage(Rhydon(), Starmie(), Earthquake()) == 146
    assert calculate_damage(Rhydon(), Jolteon(), Earthquake()) == 333  # Max HP
    assert calculate_damage(Jolteon(), Rhydon(), Thunderbolt()) == 0
    assert calculate_damage(Jolteon(), Starmie(), Thunderbolt()) == 256
