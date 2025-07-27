import numpy as np
import pytest

from dqn_agent import DQNAgent
from pokemon_battle_env import PokemonBattleEnv


class TestPokemonBattleEnv:
    def test_env_init(self):
        env = PokemonBattleEnv()
        assert env.possible_agents == ["player_0", "player_1"]
        assert env.pokemon_max_hp == [523, 383, 365]

    def test_reset(self):
        env = PokemonBattleEnv()
        env.reset()

        # Check initial state
        assert env.game_state["player_0"]["active"] == 0
        assert env.game_state["player_1"]["active"] == 0
        assert env.game_state["player_0"]["hp"] == [523, 383, 365]
        assert env.game_state["player_1"]["hp"] == [523, 383, 365]

        # Check observations
        obs = env.observe("player_0")
        assert obs.shape == (8,)
        assert obs[0] == 523  # Snorlax HP
        assert obs[1] == 383  # Zapdos HP
        assert obs[2] == 365  # Nidoking HP

    def test_action_space(self):
        env = PokemonBattleEnv()
        env.reset()

        for agent in env.agents:
            assert env.action_space(agent).n == 5

    def test_observation_space(self):
        env = PokemonBattleEnv()
        env.reset()

        for agent in env.agents:
            assert env.observation_space(agent).shape == (8,)

    def test_damage_calculation(self):
        env = PokemonBattleEnv()
        env.reset()

        # Test Snorlax vs Snorlax with Return
        damage = env.damage_table[(0, 0, 0)]
        assert damage == 166

        # Test Zapdos vs Snorlax with Thunderbolt
        damage = env.damage_table[(1, 0, 0)]
        assert damage == 123

    def test_battle_sequence(self):
        env = PokemonBattleEnv()
        env.reset()

        # Player 0 uses Return
        assert env.agent_selection == "player_0"
        env.step(0)

        # Player 1 uses Thunderbolt (but has Snorlax active, so uses Return)
        assert env.agent_selection == "player_1"
        env.step(0)

        # Check that damage was applied
        assert env.game_state["player_0"]["hp"][0] < 523
        assert env.game_state["player_1"]["hp"][0] < 523

    def test_switch_action(self):
        env = PokemonBattleEnv()
        env.reset()

        # Player 0 switches to Zapdos
        env.step(3)  # Switch to Pokemon 1 (Zapdos)

        # Player 1 switches to Zapdos
        env.step(3)  # Switch to Pokemon 1 (Zapdos)

        # Check that Pokemon were switched
        assert env.game_state["player_0"]["active"] == 1  # Zapdos
        assert env.game_state["player_1"]["active"] == 1  # Zapdos

    def test_game_end_condition(self):
        env = PokemonBattleEnv()
        env.reset()

        # Manually set one player's Pokemon to 0 HP
        env.game_state["player_1"]["hp"] = [0, 0, 0]
        env.game_state["player_1"]["fainted"] = [True, True, True]

        # Take any action to trigger game end check
        env.step(0)
        env.step(0)

        # Check that game ended
        assert all(env.terminations.values())


class TestDQNAgent:
    def test_agent_init(self):
        agent = DQNAgent(state_size=8, action_size=5)
        assert agent.state_size == 8
        assert agent.action_size == 5
        assert agent.epsilon == 1.0

    def test_act_random(self):
        agent = DQNAgent(state_size=8, action_size=5)
        state = np.random.rand(8)

        # With epsilon=1, should always return random action
        actions = [agent.act(state, training=True) for _ in range(10)]
        assert all(0 <= a < 5 for a in actions)

    def test_act_greedy(self):
        agent = DQNAgent(state_size=8, action_size=5)
        agent.epsilon = 0  # No exploration

        state = np.random.rand(8)
        action = agent.act(state, training=False)
        assert 0 <= action < 5

    def test_memory(self):
        agent = DQNAgent(state_size=8, action_size=5)

        state = np.random.rand(8)
        action = 1
        reward = 1.0
        next_state = np.random.rand(8)
        done = False

        agent.remember(state, action, reward, next_state, done)
        assert len(agent.memory) == 1

    def test_replay_insufficient_memory(self):
        agent = DQNAgent(state_size=8, action_size=5, batch_size=32)

        # Add only a few samples
        for _ in range(10):
            state = np.random.rand(8)
            action = np.random.randint(5)
            reward = np.random.randn()
            next_state = np.random.rand(8)
            done = False
            agent.remember(state, action, reward, next_state, done)

        # Should not crash with insufficient memory
        agent.replay()

    def test_epsilon_decay(self):
        agent = DQNAgent(state_size=8, action_size=5, epsilon_decay=0.95)
        initial_epsilon = agent.epsilon

        # Fill memory
        for _ in range(100):
            state = np.random.rand(8)
            action = np.random.randint(5)
            reward = np.random.randn()
            next_state = np.random.rand(8)
            done = False
            agent.remember(state, action, reward, next_state, done)

        # Trigger replay
        agent.replay()

        # Check epsilon decayed
        assert agent.epsilon < initial_epsilon


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
