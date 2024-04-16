from typing import Tuple

from numpy import ndarray

from pokemon_ai import logger
from pokemon_ai.environment.simulator.battle import Battle
from pokemon_ai.environment.simulator.player import Action, Player, RandomPlayer

StepResult = Tuple[ndarray, float, bool]


class Environment:
    battle: Battle
    agent_player: Player
    opponent: Player

    def __init__(self, agent_player=RandomPlayer(), opponent=RandomPlayer()) -> None:
        self.opponent = opponent
        self.agent_player = agent_player

    def step(self, action: Action) -> StepResult:
        result = self.battle.forward_step(action)
        state = self.battle.to_array()
        if result == "AGENT_WON":
            return (state, 1, True)
        if result == "OPPONENT_WON":
            return (state, -1, True)
        return (state, 0, False)

    def reset(self):
        # TODO: keep the setting
        # self.battle = Battle(self.agent_player, self.opponent)
        self.battle = Battle(RandomPlayer(), RandomPlayer())
        return self.battle.to_array()

    def render(self):
        logger.log(self.battle)
