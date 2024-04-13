import random
from dataclasses import dataclass
from typing import List

import numpy as np

from pokemon_ai import logger
from pokemon_ai.q_learning.environment import Environment
from pokemon_ai.simulator.battle import Battle
from pokemon_ai.simulator.player import Action

# TODO: enable to change them
ALPHA = 0.1
GAMMA = 0.9


@dataclass
class Experience:
    state: np.ndarray
    action: Action
    reward: float


class Agent:
    epsilon: float
    Q: np.ndarray

    def __init__(self, epsilon: float = 0.1) -> None:
        self.epsilon = epsilon
        state_space = 4
        action_space = 2
        self.Q = np.zeros((state_space, action_space))

    def learn(self, env: Environment, episodes: int):
        num_of_win = 0
        experiences: List[Experience] = []
        for episode in range(episodes):
            state = env.reset()
            while True:
                action = self.policy(state)
                next_state, reward, terminated = env.step(action)
                state = next_state
                experiences.append(Experience(state=state, action=action, reward=reward))
                if terminated:
                    if reward > 0:
                        num_of_win += 1
                    break
            if episode % 100 == 0:
                print("win rate:", num_of_win / (episode + 1))
                # print(experiences)
            # TODO: q learning

    def policy(self, state: np.ndarray) -> Action:
        # By defualt, random move
        action = random.choice(
            [
                Action.MOVE_0,
                Action.MOVE_1,
            ]
        )
        if random.random() > self.epsilon:
            # Implment e-greedy
            pass
        return action
