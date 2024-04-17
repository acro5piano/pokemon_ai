from random import seed

from pokemon_ai.environment.environment import Environment
from pokemon_ai.environment.simulator.player import Action, RandomPlayer

seed(42)


def test_environment():
    env = Environment(RandomPlayer(), RandomPlayer())
    env.step(Action.MOVE_0)
    assert 1 == 1
