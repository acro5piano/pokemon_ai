import random
from dataclasses import dataclass

from pokemon_ai import logger
from pokemon_ai.q_learning.environment import Environment
from pokemon_ai.simulator.battle import Battle
from pokemon_ai.simulator.player import Action

State = int  # TODO


@dataclass
class Experience:
    state: State
    action: Action
    reward: float


class Agent:
    epsilon: float

    def __init__(self, epsilon: float) -> None:
        self.epsilon = epsilon

    def learn(self, env: Environment, episodes: int):
        for step in range(episodes):
            experience = []
            if step % 100 == 0:
                env.render()
            while True:
                action = 0
                env.step(action)

    def policy(self, state: State):
        # TODO: implement this
        return random.choice(
            [
                Action.CHANGE_TO_0,
                Action.CHANGE_TO_1,
                Action.MOVE_0,
            ]
        )
