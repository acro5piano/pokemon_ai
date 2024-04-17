import random

from pokemon_ai.simulator.action import Action
from pokemon_ai.simulator.dex import Snorlax
from pokemon_ai.simulator.player import Player

random.seed(42)


def test_player():
    player = Player([Snorlax()])
    assert player.possible_actions() == [
        Action.MOVE_0,
        Action.MOVE_1,
    ]
    player.pokemons[0].hp = 0
    player.reset()
    assert player.pokemons[0].hp == 523
