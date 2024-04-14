import random
from collections import defaultdict
from dataclasses import dataclass
from pprint import pprint
from typing import Dict, List

import numpy as np
from numpy.lib import math

from pokemon_ai import logger
from pokemon_ai.q_learning.environment import Environment
from pokemon_ai.simulator.battle import Battle
from pokemon_ai.simulator.player import Action

# TODO: enable to change them
ALPHA = 0.1
GAMMA = 0.9


STATE_SPACE = 4
ACTION_SPACE = 2

State = tuple[int, int, int, int]
#       Q    State      Action  Reward
#       |    |            |     |
QType = dict[State, dict[int, int]]


@dataclass
class Experience:
    state: State
    action: Action
    reward: float


class Agent:
    epsilon: float
    # Q: np.ndarray
    Q: QType

    def __init__(self, epsilon: float = 0.1) -> None:
        self.epsilon = epsilon
        # self.Q = np.zeros((STATE_SPACE, ACTION_SPACE))
        # self.Q = defaultdict(lambda: [0] * 4)
        self.Q = {}

    def learn(self, env: Environment, episodes: int):
        num_of_win = 0
        N: QType = {}
        for episode in range(episodes):
            experiences: List[Experience] = []
            state = env.reset()
            while True:
                action = self.policy(state)
                next_state, reward, terminated = env.step(action)
                state = next_state
                experiences.append(Experience(state=tuple(state), action=action, reward=reward))
                if terminated:
                    if reward > 0:
                        num_of_win += 1
                    break

            # if episode % 100 == 0:
            #     print("win rate:", num_of_win / (episode + 1))
            # print(experiences)

            for i, x in enumerate(experiences):
                G, t = 0, 0
                for j in range(i, len(experiences)):
                    G += math.pow(GAMMA, t) * experiences[j].reward
                    t += 1
                s = tuple(x.state)
                a = x.action.value
                if not s in N:
                    N[s] = [0] * ACTION_SPACE
                N[s][a] += 1

                alpha = 1 / N[s][a]
                if not s in self.Q:
                    print("here", s)
                    self.Q[s] = [0] * ACTION_SPACE
                self.Q[s][a] += alpha * (G - self.Q[s][a])
            # TODO: q learning

    def policy(self, state: np.ndarray) -> Action:
        actions = [
            Action.MOVE_0,
            Action.MOVE_1,
        ]
        if random.random() < self.epsilon or tuple(state) not in self.Q:
            return random.choice(actions)
        else:
            index = np.argmax(self.Q[tuple(state)])
            return actions[index]

    def play(self, env: Environment):
        self.epsilon = 0
        state = env.reset()
        pprint(self.Q)
        print(state)
        while True:
            action = self.policy(state)
            print(action)
            next_state, reward, terminated = env.step(action)
            print(next_state)
            state = next_state
            if terminated:
                if reward > 0:
                    print("won")
                else:
                    print("lose")
                break
