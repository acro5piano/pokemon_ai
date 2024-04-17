import math
import random
from dataclasses import dataclass
from pprint import pprint

import numpy as np

from pokemon_ai.learning.environment import Environment
from pokemon_ai.simulator.player import Action

# TODO: enable to change them
ALPHA = 0.1
GAMMA = 0.9


ACTION_SPACE = 2

State = tuple[int, int, int, int]
#       Q    State      Action  Reward
#       |    |            |     |
QType = dict[State, list[float]]


@dataclass
class Experience:
    state: State
    action: Action
    reward: float


def array_to_state(array: np.ndarray) -> State:
    return tuple(array)  # type: ignore


class MonteCarloAgent:
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
            experiences: list[Experience] = []
            state = env.reset()
            while True:
                action = self.policy(state)
                next_state, reward, terminated = env.step(action)
                experiences.append(
                    Experience(state=array_to_state(state), action=action, reward=reward)
                )
                state = next_state
                if terminated:
                    if reward > 0:
                        num_of_win += 1
                    break

            if episode % 100 == 0:
                print("win rate:", num_of_win / (episode + 1))

            for i, x in enumerate(experiences):
                G, t = 0, 0
                for j in range(i, len(experiences)):
                    G += math.pow(GAMMA, t) * experiences[j].reward
                    t += 1
                s = x.state
                a = x.action.value
                if not s in self.Q:
                    self.Q[s] = [0] * ACTION_SPACE
                if not s in N:
                    N[s] = [0] * ACTION_SPACE
                N[s][a] += 1
                alpha = 1 / N[s][a]
                self.Q[s][a] += alpha * (G - self.Q[s][a])

    def policy(
        self,
        state: np.ndarray,
    ) -> Action:
        actions = [action for action in Action]
        s = array_to_state(state)
        if random.random() < self.epsilon or s not in self.Q:
            return random.choice(actions)
        else:
            index = np.argmax(self.Q[s])
            return actions[index]

    def play(self, env: Environment):
        self.epsilon = 0
        state = env.reset()
        pprint(self.Q)
        pprint(state)
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
