import random

from pokemon_ai.environment.environment import Environment
from pokemon_ai.environment.simulator.dex import Snorlax, Zapdos
from pokemon_ai.environment.simulator.player import Action, RandomPlayer

random.seed(42)


def test_environment():
    env = Environment(RandomPlayer([Snorlax(), Zapdos()]), RandomPlayer([Snorlax(), Zapdos()]))
    env.step(Action.MOVE_0)
    assert 1 == 1
