from typing import Tuple

from numpy import ndarray

from pokemon_ai import logger
from pokemon_ai.simulator.battle import Battle, BattleResult
from pokemon_ai.simulator.dex import Snorlax
from pokemon_ai.simulator.player import Action, Player

StepResult = Tuple[ndarray, float, bool]


class Environment:
    battle: Battle
    opponent: Player

    def __init__(self, opponent: Player) -> None:
        self.battle = Battle(Player([Snorlax()]), opponent)
        self.opponent = opponent

    def step(self, action: Action) -> StepResult:
        result = self.battle.forward_step(action, self.opponent.choose_action())
        state = self.battle.to_array()
        if result == BattleResult.PLAYER1_WON:
            return (state, 1, True)
        if result == BattleResult.PLAYER2_WON:
            return (state, -1, True)
        return (state, 0, False)

    def reset(self):
        # TODO: keep the setting
        # self.battle = Battle(self.agent_player, self.opponent)
        self.battle.reset()
        return self.battle.to_array()

    def render(self):
        logger.log(self.battle)
