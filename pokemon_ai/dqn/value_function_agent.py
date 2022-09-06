from random import random, sample
from typing import Optional

import numpy as np
from sklearn.neural_network import MLPRegressor

import pokemon_ai.simulator.moves as m
import pokemon_ai.simulator.pokedex as p
from pokemon_ai.dqn.experience import Experience
from pokemon_ai.simulator.battle_simplified import Battle
from pokemon_ai.simulator.player import Action, Player

GAMMA = 0.9


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
    epsilon: float

    def __init__(
        self,
        model: MLPRegressor,
        epsilon: float,
    ):
        self.model = model
        self.pokemons = build_random_team()
        self.epsilon = epsilon
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
        if random() < self.epsilon:
            if random() < 0.5:
                return Action.FIGHT
            else:
                return Action.CHANGE
        action = self.model.predict([[*self.to_array(), *opponent.to_array()]])
        return Action(action[0].argmax())

    def choose_action_on_pokemon_dead(self, opponent: Player) -> Action:
        return Action.CHANGE


class ValueFunctionAgent:
    # model: Pipeline
    model: MLPRegressor
    battle: Battle
    learner: Player
    opponent: Player
    epsilon: float

    def __init__(
        self,
        model: Optional[MLPRegressor] = None,
        epsilon: float = 0.2,
    ):
        if model:
            self.model = model
        else:
            self.model = MLPRegressor(
                hidden_layer_sizes=(10, 10),
                max_iter=200,
            )
        self.epsilon = epsilon
        fake_state = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
        fake_estimation = np.array([[0, 0]])
        self.model.partial_fit(fake_state, fake_estimation)

    def reset(self):
        self.learner = NeuralNetworkPlayer(self.model, self.epsilon)
        self.opponent = StupidRandomPlayer(build_random_team())

    def update(self, experiences: list[Experience]):
        states = np.array([e.state for e in experiences])
        next_states = np.array([e.next_state for e in experiences])

        y = self.model.predict(states)
        future = self.model.predict(next_states)

        for i, experience in enumerate(experiences):
            reward = experience.reward
            if not experience.done:
                reward += GAMMA * np.max(future[i])
            y[i][experience.action.value] = reward

        self.model.partial_fit(states, y)


def build_random_team() -> list[p.Pokemon]:
    pokemons = [
        p.Jolteon([m.Thunderbolt()]),
        p.Rhydon([m.Earthquake()]),
        p.Starmie([m.Surf()]),
    ]
    return sample(pokemons, 2)
