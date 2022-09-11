import logging
from random import random
from typing import Optional

import numpy as np
from sklearn.neural_network import MLPRegressor

import pokemon_ai.simulator.pokedex as p
from pokemon_ai.dqn.experience import Experience
from pokemon_ai.dqn.utils import build_random_team
from pokemon_ai.simulator.battle import Battle
from pokemon_ai.simulator.player import Action, Player
from pokemon_ai.simulator.sample_players import JustAttackPlayer, StupidRandomPlayer

GAMMA = 0.9


class NeuralNetworkPlayer(Player):
    model: MLPRegressor
    epsilon: float

    def __init__(
        self,
        pokemons: list[p.Pokemon],
        model: MLPRegressor,
        epsilon: float,
    ):
        self.pokemons = pokemons
        self.model = model
        self.epsilon = epsilon

    def choose_action(self, opponent: Player) -> Action:
        available_pokemons = self.get_available_pokemons_for_change()
        if random() < self.epsilon:
            if len(available_pokemons) == 0 or random() < 0.5:
                return self.pick_random_move_action()
            else:
                return Action.change_to(self.get_random_living_pokemon_index_to_replace())
        predicts = self.model.predict([[*self.to_array(), *opponent.to_array()]])[0]
        for index, _ in enumerate(predicts):
            if index < 6 and (
                self.pokemons[index].actual_hp <= 0 or index == self.active_pokemon_index
            ):
                predicts[index] = predicts.min() - 1
        logging.info(f"predictions:\n{predicts}")
        return Action(predicts.argmax())

    def choose_action_on_pokemon_dead(self, opponent: Player) -> Action:
        if random() < self.epsilon:
            return Action.change_to(self.get_random_living_pokemon_index_to_replace())
        else:
            predicts_arr = self.model.predict([[*self.to_array(), *opponent.to_array()]])
            predicts = predicts_arr[0][:6]  # [:6] removes skill moves
            for index in range(0, len(self.pokemons)):
                if self.pokemons[index].actual_hp <= 0 or index == self.active_pokemon_index:
                    predicts[index] = predicts.min() - 1
            logging.info(f"predictions:\n{predicts}")
            return Action(predicts.argmax())


# TODO: create a team from neural network. How to do it???
# Maybe we can calculate team's win rate and use it as learning data
# if random() < EPSILON:
#     self.pokemons = build_random_team()
# else:
#     self.pokemons


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
        # pokemon(id + is_active + actual_hp + 4 moves) * 8, 2 players
        fake_state = np.array([np.zeros((7 * 6) * 2)])
        fake_estimation = np.array([np.zeros(10)])  # change * 6, moves * 4
        self.model.partial_fit(fake_state, fake_estimation)

    def reset(self, max_episodes: int, episodes: int):
        self.learner = NeuralNetworkPlayer(
            build_random_team(),
            self.model,
            self.epsilon,
        )

        # Curriculum learning: use random player at the beginning
        if episodes / max_episodes < random():
            self.opponent = StupidRandomPlayer(build_random_team())
        else:
            self.opponent = JustAttackPlayer(build_random_team())

        # TODO: Actually we want to use an opponent which is also a neural network,
        # But it requires to change the simulator to support multiple neural network players
        # Like symmetrical battle and reward should be calculated by both players
        # self.opponent = NeuralNetworkPlayer(self.model, self.epsilon)

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
