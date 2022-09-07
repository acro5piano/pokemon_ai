from random import seed

from pokemon_ai.simulator.player import Player
from pokemon_ai.simulator.pokedex import Jolteon, Rhydon, Starmie


def test_player_random_action():
    seed(4)
    player = Player([Jolteon(), Rhydon(), Starmie(), Jolteon()])
    player.pokemons[1].actual_hp = 0
    for _ in range(0, 100):
        assert player.get_random_living_pokemon_index_to_replace() in [2, 3]
