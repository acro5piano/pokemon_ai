from typing import Tuple

from pokemon_ai import logger
from pokemon_ai.simulator.battle import Battle
from pokemon_ai.simulator.player import Action, Player, RandomPlayer


class Environment:
    battle: Battle
    opponent: Player

    def __init__(self, opponent=RandomPlayer()) -> None:
        self.opponent = opponent

    def step(self, action: Action):
        self.battle.forward_step(action)
        # TODO: define them
        return (self.battle.to_array(), 1, False)

    def reset(self):
        self.battle = Battle(self.opponent)
        return self.battle.to_array()

    def render(self):
        logger.log(self.battle)
