import logging
from random import random, sample
from typing import Any, Optional

import numpy as np
import tensorflow as tf
from sklearn.neural_network import MLPRegressor

import pokemon_ai.simulator.moves as m
import pokemon_ai.simulator.pokedex as p
from pokemon_ai.dqn.experience import Experience
from pokemon_ai.dqn.opponents import JustAttackPlayer
from pokemon_ai.simulator.battle_simplified import Battle
from pokemon_ai.simulator.player import Action, Player

GAMMA = 0.9

SHAPE = (37, 2, 1)


def reshape_states(states: np.ndarray) -> np.ndarray:
    return np.array([state.reshape(SHAPE) for state in states])


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
        if len(available_pokemons) == 0:
            return self.pick_random_move_action()
        if random() < self.epsilon:
            if random() < 0.5:
                return self.pick_random_move_action()
            else:
                return Action.change_to(self.get_random_living_pokemon_index_to_replace())
        X = reshape_states(np.array([[*self.to_array(), *opponent.to_array()]]))
        predicts = self.model.predict(X)[0]
        for index, _ in enumerate(predicts):
            if index < 6:
                if self.pokemons[index].actual_hp <= 0 or index == self.active_pokemon_index:
                    predicts[index] = predicts.min() - 1
        logging.info(f"predictions:\n{predicts}")
        return Action(predicts.argmax())

    def choose_action_on_pokemon_dead(self, opponent: Player) -> Action:
        if random() < self.epsilon:
            return Action.change_to(self.get_random_living_pokemon_index_to_replace())
        else:
            X = reshape_states(np.array([[*self.to_array(), *opponent.to_array()]]))
            predicts_arr = self.model.predict(X)
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
    model: Any
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
            cnn = tf.keras.Sequential(
                [
                    tf.keras.layers.Conv2D(
                        5,
                        kernel_size=3,
                        strides=1,
                        padding="same",
                        activation="relu",
                        input_shape=SHAPE,
                    ),
                    tf.keras.layers.Conv2D(
                        3,
                        kernel_size=2,
                        strides=1,
                        padding="same",
                        activation="relu",
                    ),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(units=10, activation="softmax"),
                ]
            )
            cnn.compile(optimizer="sgd", loss="categorical_crossentropy")
            self.model = cnn
        self.epsilon = epsilon

    def reset(self):
        self.learner = NeuralNetworkPlayer(
            [
                p.Jolteon([m.Thunderbolt(), m.BodySlam(), m.DoubleKick(), m.PinMissle()]),
                p.Starmie([m.Surf(), m.Blizzard(), m.Psychic(), m.Thunderbolt()]),
                p.Jolteon([m.Thunderbolt(), m.BodySlam(), m.DoubleKick(), m.PinMissle()]),
                p.Rhydon([m.Earthquake(), m.RockSlide(), m.Surf(), m.BodySlam()]),
                p.Starmie([m.Surf(), m.Blizzard(), m.Psychic(), m.Thunderbolt()]),
                p.Starmie([m.Surf(), m.Blizzard(), m.Psychic(), m.Thunderbolt()]),
            ],
            self.model,
            self.epsilon,
        )

        # self.opponent = StupidRandomPlayer(build_random_team())

        self.opponent = JustAttackPlayer(
            [
                p.Rhydon([m.Earthquake(), m.RockSlide(), m.Surf(), m.BodySlam()]),
                p.Rhydon([m.Earthquake(), m.RockSlide(), m.Surf(), m.BodySlam()]),
                p.Starmie([m.Surf(), m.Blizzard(), m.Psychic(), m.Thunderbolt()]),
                p.Jolteon([m.Thunderbolt(), m.BodySlam(), m.DoubleKick(), m.PinMissle()]),
                p.Jolteon([m.Thunderbolt(), m.BodySlam(), m.DoubleKick(), m.PinMissle()]),
                p.Starmie([m.Surf(), m.Blizzard(), m.Psychic(), m.Thunderbolt()]),
            ]
        )

        # TODO: Actually we want to use an opponent which is also a neural network,
        # But it requires to change the simulator to support multiple neural network players
        # Like symmetrical battle and reward should be calculated by both players
        # self.opponent = NeuralNetworkPlayer(self.model, self.epsilon)

    def update(self, experiences: list[Experience]):
        states = np.array([e.state for e in experiences])
        next_states = np.array([e.next_state for e in experiences])

        y = self.model.predict(reshape_states(states))
        future = self.model.predict(reshape_states(next_states))

        for i, experience in enumerate(experiences):
            reward = experience.reward
            if not experience.done:
                reward += GAMMA * np.max(future[i])
            y[i][experience.action.value] = reward

        X = np.array([state.reshape(SHAPE) for state in states])
        self.model.train_on_batch(X, y)


def build_random_team() -> list[p.Pokemon]:
    pokemons = [
        p.Jolteon([m.Thunderbolt(), m.BodySlam(), m.DoubleKick(), m.PinMissle()]),
        p.Jolteon([m.Thunderbolt(), m.BodySlam(), m.DoubleKick(), m.PinMissle()]),
        p.Jolteon([m.Thunderbolt(), m.BodySlam(), m.DoubleKick(), m.PinMissle()]),
        p.Rhydon([m.Earthquake(), m.RockSlide(), m.Surf(), m.BodySlam()]),
        p.Rhydon([m.Earthquake(), m.RockSlide(), m.Surf(), m.BodySlam()]),
        p.Rhydon([m.Earthquake(), m.RockSlide(), m.Surf(), m.BodySlam()]),
        p.Starmie([m.Surf(), m.Blizzard(), m.Psychic(), m.Thunderbolt()]),
        p.Starmie([m.Surf(), m.Blizzard(), m.Psychic(), m.Thunderbolt()]),
        p.Starmie([m.Surf(), m.Blizzard(), m.Psychic(), m.Thunderbolt()]),
    ]
    return sample(pokemons, 6)
