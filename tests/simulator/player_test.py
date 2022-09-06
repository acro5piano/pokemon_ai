from random import seed

from pokemon_ai.simulator.player import Player
from pokemon_ai.simulator.pokedex import Jolteon, Rhydon, Starmie


def test_get_random_living_pokemon_index():
    seed(4)
    player = Player([Jolteon(), Rhydon(), Starmie()])
    player.get_active_pokemon().actual_hp = 0
    assert player.get_random_living_pokemon_index() == 1
    assert player.get_random_living_pokemon_index() == 1
    assert player.get_random_living_pokemon_index() == 2
    assert player.get_random_living_pokemon_index() == 1


def test_player_random_action():
    seed(4)
    player = Player([Jolteon(), Rhydon(), Starmie()])
    player.pokemons[1].actual_hp = 0
    assert player.get_random_living_pokemon_index_to_replace() == 2
    assert player.get_random_living_pokemon_index_to_replace() == 2
    assert player.get_random_living_pokemon_index_to_replace() == 2
    assert player.get_random_living_pokemon_index_to_replace() == 2
    assert player.get_random_living_pokemon_index_to_replace() == 2
    assert player.get_random_living_pokemon_index_to_replace() == 2
