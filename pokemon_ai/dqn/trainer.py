import logging
from collections import deque
from random import sample
from typing import Optional

from sklearn.neural_network import MLPRegressor

from pokemon_ai.dqn.experience import Experience
from pokemon_ai.dqn.value_function_agent import ValueFunctionAgent
from pokemon_ai.simulator.battle_simplified import Battle


class Trainer:
    step = 0
    experiences = deque(maxlen=1024)

    def __init__(self, episodes: int, model: Optional[MLPRegressor] = None, epsilon: float = 0.2):
        self.agent = ValueFunctionAgent(model=model, epsilon=epsilon)
        self.episodes = episodes

    def train(self):
        win_count_total = 0
        win_count_of_100 = 0
        for episode in range(0, self.episodes):
            self.agent.reset()
            battle = Battle(self.agent.learner, self.agent.opponent)
            battle.validate()
            logging.info(battle)
            while True:
                logging.info(f"=== turn {battle.turn} ===")
                current_state = battle.to_array()

                current_learner_pokemon_count = len(battle.player1.get_available_pokemons())
                current_opponent_pokemon_count = len(battle.player2.get_available_pokemons())

                action, _ = battle.forward_step()
                winner = battle.get_winner()

                next_learner_pokemon_count = len(battle.player1.get_available_pokemons())
                next_opponent_pokemon_count = len(battle.player2.get_available_pokemons())

                if action is not None:
                    reward = 0
                    if winner == self.agent.learner:
                        logging.info(f"learner won the battle!")
                        reward = 1
                    if winner == self.agent.opponent:
                        logging.info(f"learner lost...")
                        reward = -1
                    if battle.turn > 500:
                        logging.info("battle is too long")
                        reward = -0.1
                    if current_opponent_pokemon_count > next_opponent_pokemon_count:
                        reward += 0.3
                    if current_learner_pokemon_count > next_learner_pokemon_count:
                        reward -= 0.3
                    self.experiences.append(
                        Experience(
                            state=current_state,
                            action=action,
                            reward=reward,
                            next_state=battle.to_array(),
                            done=winner is not None,
                        )
                    )
                self.step += 1
                logging.info(battle)
                if winner is not None or battle.turn > 500:
                    if winner == self.agent.learner:
                        win_count_total += 1
                        win_count_of_100 += 1
                    break
            if len(self.experiences) > 64:
                self.agent.update(sample(self.experiences, 64))
            if episode > 0 and episode % 100 == 0:
                print(f"=============")
                print(f"episode {episode}")
                print(f"Win Rate of 100: {win_count_of_100 / 100}")
                print(f"Total Win Rate: {win_count_total / episode}")
                win_count_of_100 = 0
        print(f"=======================================")
        print(f"Total Win Count: {win_count_total}")
        print(f"Total Win Rate: {win_count_total / self.episodes}")
