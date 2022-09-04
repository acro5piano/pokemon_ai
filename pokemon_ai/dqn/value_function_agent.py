from collections import deque, namedtuple
from random import random, sample

import numpy as np
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

import pokemon_ai.simulator.moves as m
import pokemon_ai.simulator.pokedex as p
from pokemon_ai.logger import log
from pokemon_ai.simulator.battle import Battle
from pokemon_ai.simulator.player import Action, ActionChangeTo, ActionSelectMove, Player
from pokemon_ai.simulator.sample_players import StupidRandomPlayer

EPSILON = 0.2
GAMMA = 0.9


Experience = namedtuple("Experience", ["state", "action", "reward", "next_state", "done"])


class NeuralNetworkPlayer(Player):
    model: Pipeline

    def __init__(self, model: Pipeline):
        self.model = model
        self.pokemons = build_random_team()
        # TODO: create a team from neural network. How to do it???
        # if random() < EPSILON:
        #     self.pokemons = build_random_team()
        # else:
        #     self.pokemons

    def choose_action(self, opponent: Player) -> Action:
        available_pokemons = self.get_available_pokemons_for_change()
        if len(available_pokemons) == 0:
            return ActionSelectMove(self.get_active_pokemon().actual_moves[0])
        if random() < EPSILON:
            if random() < 0.5:
                return ActionSelectMove(self.get_active_pokemon().actual_moves[0])
            else:
                return ActionChangeTo(available_pokemons[0])
        action = self.model.predict([*self.to_array(), *opponent.to_array()])
        print(action)
        return action

    def choose_action_on_pokemon_dead(self, opponent: Player) -> ActionChangeTo:
        return ActionChangeTo(self.get_available_pokemons()[0])


class ValueFunctionAgent:
    model: Pipeline
    battle: Battle
    learner: Player
    opponent: Player

    def __init__(self):
        self.model = Pipeline(
            [
                ("scaler", StandardScaler()),
                (
                    "mlp",
                    MLPRegressor(
                        hidden_layer_sizes=(10, 10),
                        max_iter=1,
                    ),
                ),
            ]
        )

    def reset(self):
        self.learner = NeuralNetworkPlayer(self.model)
        self.opponent = StupidRandomPlayer(build_random_team())

    def update(self, experiences: deque[Experience]):
        states = np.vstack([e.state for e in experiences])
        next_states = np.vstack([e.next_state for e in experiences])
        future = self.model.predict(next_states)
        y = self.model.predict(states)

        for i, experience in enumerate(experiences):
            reward = experience.reward
            if not experience.done:
                reward += GAMMA * np.max(future[i])
            y[i, experience.action] = reward

        X = self.model.named_steps("scaler").transform(states)
        self.model.named_steps("mlp").partial_fit(X, y)


def build_random_team() -> list[p.Pokemon]:
    pokemons = [
        p.Jolteon([m.Thunderbolt()]),
        p.Rhydon([m.Earthquake()]),
        p.Starmie([m.Surf()]),
    ]
    return sample(pokemons, 2)


class Trainer:
    def __init__(self):
        self.agent = ValueFunctionAgent()
        self.experiences = deque(maxlen=1024)

    def train(self):
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
            if winner is not None:
                break
            if battle.turn > 500:
                log("battle is too long")
                break
            log(battle)
