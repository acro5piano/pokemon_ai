import random

from pokemon_ai.learning.environment import Environment
from pokemon_ai.learning.monte_carlo_agent import MonteCarloAgent
from pokemon_ai.learning.players import RandomPlayer
from pokemon_ai.simulator.action import Action
from pokemon_ai.simulator.dex import Snorlax

random.seed(42)


def test_environment():
    env = Environment(RandomPlayer([Snorlax()]))
    env.step(Action.MOVE_0)
    assert 1 == 1
