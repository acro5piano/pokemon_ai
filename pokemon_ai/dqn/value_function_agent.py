from collections import deque
from dataclasses import dataclass
from random import random, sample

import numpy as np
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

import pokemon_ai.simulator.moves as m
import pokemon_ai.simulator.pokedex as p
from pokemon_ai.logger import log
from pokemon_ai.simulator.battle_simplified import Battle
from pokemon_ai.simulator.player import Action, Player

EPSILON = 0.2
GAMMA = 0.9


# TODO: use dataclass
# Experience = namedtuple("Experience", ["state", "action", "reward", "next_state", "done"])


@dataclass
class Experience:
    state: list[int]
    action: Action
    reward: float
    next_state: list[int]
    done: bool


class StupidRandomPlayer(Player):
    def choose_action(self, opponent: Player) -> Action:
        available_pokemons = self.get_available_pokemons_for_change()
        if len(available_pokemons) == 0:
            return Action.FIGHT
        if random() < 0.5:
            return Action.FIGHT
        else:
            return Action.CHANGE


class NeuralNetworkPlayer(Player):
    model: MLPRegressor

    def __init__(self, model: MLPRegressor, step: int):
        self.model = model
        self.pokemons = build_random_team()
        self.step = step
        # TODO: create a team from neural network. How to do it???
        # Maybe we can calculate team's win rate and use it as learning data

        # if random() < EPSILON:
        #     self.pokemons = build_random_team()
        # else:
        #     self.pokemons

    def choose_action(self, opponent: Player) -> Action:
        available_pokemons = self.get_available_pokemons_for_change()
        if len(available_pokemons) == 0:
            return Action.FIGHT
        if self.step == 0 or random() < EPSILON:
            if random() < 0.5:
                return Action.FIGHT
            else:
                return Action.CHANGE
        action = self.model.predict([*self.to_array(), *opponent.to_array()])
        print(action)
        return action

    def choose_action_on_pokemon_dead(self, opponent: Player) -> Action:
        return Action.CHANGE


class ValueFunctionAgent:
    # model: Pipeline
    model: MLPRegressor
    battle: Battle
    learner: Player
    opponent: Player

    def __init__(self, step: int):
        # self.model = Pipeline(
        #     [
        #         (
        #             "mlp",
        #             MLPRegressor(
        #                 hidden_layer_sizes=(10, 10),
        #                 max_iter=1,
        #             ),
        #         ),
        #     ]
        # )
        self.model = MLPRegressor(
            hidden_layer_sizes=(10, 10),
            max_iter=10000,
        )
        self.step = step
        fake_state = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
        fake_estimation = np.array([[0, 0]])
        self.model.partial_fit(fake_state, fake_estimation)

    def reset(self):
        self.learner = NeuralNetworkPlayer(self.model, self.step)
        self.opponent = StupidRandomPlayer(build_random_team())

    def update(self, experiences: deque[Experience]):
        states = np.array([e.state for e in experiences])
        next_states = np.array([e.next_state for e in experiences])

        y = self.model.predict(states)
        future = self.model.predict(next_states)

        for i, experience in enumerate(experiences):
            reward = experience.reward
            if not experience.done:
                reward += GAMMA * np.max(future[i])
            # action[0] = action type,
            # action[1] = action content,
            y[i][experience.action.value] = reward

        self.model.partial_fit(states, y)


def build_random_team() -> list[p.Pokemon]:
    pokemons = [
        p.Jolteon([m.Thunderbolt()]),
        p.Rhydon([m.Earthquake()]),
        p.Starmie([m.Surf()]),
    ]
    return sample(pokemons, 2)


class Trainer:
    step = 0
    experiences = deque(maxlen=1024)

    def __init__(self, episodes: int):
        self.agent = ValueFunctionAgent(self.step)
        self.episodes = episodes

    def train(self):
        win_count = 0
        for _ in range(0, self.episodes):
            self.agent.reset()
            battle = Battle(self.agent.learner, self.agent.opponent)
            battle.validate()
            log(battle)
            while True:
                log("")
                current_state = battle.to_array()
                action, _ = battle.forward_step()
                winner = battle.get_winner()
                if action is not None:
                    reward = 0
                    if winner == self.agent.learner:
                        log(f"learner won the battle!")
                        reward = 1
                        win_count += 1
                    if winner == self.agent.opponent:
                        log(f"learner lost...")
                        reward = -1
                    self.experiences.append(
                        Experience(
                            state=current_state,
                            action=action,
                            reward=reward,
                            next_state=battle.to_array(),
                            done=winner is not None,
                        )
                    )
                    # # This is required to fit before predicting.
                    # if self.step == 0:
                    #     states = np.vstack([e.state for e in self.experiences])
                    #     self.agent.model.named_steps["scaler"].fit(states)
                    #     self.agent.update(self.experiences)
                self.step += 1
                log(battle)
                if winner is not None:
                    break
                if battle.turn > 500:
                    log("battle is too long")
                    break
            self.agent.update(self.experiences)
        print(f"win count: {win_count}")
