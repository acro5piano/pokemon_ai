from typing import Tuple

from numpy import ndarray

from pokemon_ai import logger
from pokemon_ai.environment.simulator.battle import Battle, BattleResult
from pokemon_ai.environment.simulator.dex import Snorlax, Zapdos
from pokemon_ai.environment.simulator.player import Action, Player, RandomPlayer

StepResult = Tuple[ndarray, float, bool]


class Environment:
    battle: Battle
    agent_player: Player
    opponent: Player

    def __init__(self, agent_player, opponent) -> None:
        self.battle = Battle(
            RandomPlayer([Snorlax(), Zapdos()]), RandomPlayer([Snorlax(), Zapdos()])
        )
        self.agent_player = agent_player
        self.opponent = opponent

    def step(self, action: Action) -> StepResult:
        result = self.battle.forward_step(action)
        state = self.battle.to_array()
        if result == BattleResult.AGENT_WON:
            return (state, 1, True)
        if result == BattleResult.OPPONENT_WON:
            return (state, -1, True)
        return (state, 0, False)

    def reset(self):
        # TODO: keep the setting
        # self.battle = Battle(self.agent_player, self.opponent)
        self.battle = Battle(
            RandomPlayer([Snorlax(), Zapdos()]), RandomPlayer([Snorlax(), Zapdos()])
        )
        return self.battle.to_array()

    def render(self):
        logger.log(self.battle)
