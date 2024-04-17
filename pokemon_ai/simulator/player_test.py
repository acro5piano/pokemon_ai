import random

from pokemon_ai.environment.environment import Environment
from pokemon_ai.environment.simulator.dex import Snorlax, Zapdos
from pokemon_ai.environment.simulator.player import Action, Player, RandomPlayer

random.seed(42)


def test_environment():
    player = Player([Snorlax(), Zapdos()])
    assert player.possible_actions() == [
        Action.MOVE_0,
        Action.MOVE_1,
        Action.CHANGE_TO_1,
    ]
    assert player.active_pokemon().__class__ == Snorlax
    player.active_pokemon().hp -= Snorlax().hp
    assert player.possible_actions() == [
        Action.MOVE_0,
        Action.MOVE_1,
        Action.CHANGE_TO_1,
    ]
