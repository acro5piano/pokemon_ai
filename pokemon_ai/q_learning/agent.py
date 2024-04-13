import random
from dataclasses import dataclass
from typing import List

from numpy import ndarray

from pokemon_ai import logger
from pokemon_ai.q_learning.environment import Environment
from pokemon_ai.simulator.battle import Battle
from pokemon_ai.simulator.player import Action

# TODO: enable to change them
ALPHA = 0.1
GAMMA = 0.9


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
        num_of_win = 0.0
        for episode in range(episodes):
            state = env.reset()
            # print(state)
            experiences: List[Experience] = []
            while True:
                action = self.policy(state)
                next_state, reward, terminated = env.step(action)
                # print(state, reward, terminated)
                state = next_state
                experiences.append(Experience(state=state, action=action, reward=reward))
                if terminated:
                    if reward > 0:
                        num_of_win += 1
                    break
            if episode % 100 == 0:
                print("win rate:", num_of_win / (episode + 1))
            # print(experiences)
            # TODO: monte-carlo learning

    def policy(self, state: ndarray):
        # TODO: implement this
        return random.choice(
            [
                Action.MOVE_0,
                Action.MOVE_1,
            ]
        )
