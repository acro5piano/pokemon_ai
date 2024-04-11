import random
from dataclasses import dataclass
from typing import List

from numpy import ndarray

from pokemon_ai import logger
from pokemon_ai.q_learning.environment import Environment
from pokemon_ai.simulator.battle import Battle
from pokemon_ai.simulator.player import Action


@dataclass
class Experience:
    state: ndarray
    action: Action
    reward: float


class Agent:
    epsilon: float

    def __init__(self, epsilon: float) -> None:
        self.epsilon = epsilon

    def learn(self, env: Environment, episodes: int):
        for step in range(episodes):
            state = env.reset()
            experiences: List[Experience] = []
            if step % 100 == 0:
                env.render()
            while True:
                action = self.policy(state)
                experience = Experience(state=state, action=action, reward=0)
                state, reward, terminated = env.step(action)
                experience.reward = reward
                experiences.append(experience)
                if terminated:
                    break
            # TODO: monte-carlo learning

    def policy(self, state: ndarray):
        # TODO: implement this
        return random.choice(
            [
                Action.CHANGE_TO_0,
                Action.CHANGE_TO_1,
                Action.MOVE_0,
            ]
        )
