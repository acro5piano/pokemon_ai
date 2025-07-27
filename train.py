import os
from collections import deque

import matplotlib.pyplot as plt
import numpy as np
import torch

from dqn_agent import DQNAgent
from pokemon_battle_env import PokemonBattleEnv


def train_pokemon_dqn(episodes=1000, save_interval=100):
    # Create environment
    env = PokemonBattleEnv(render_mode=None)

    # Create agents for both players
    state_size = 8  # Observation space size (3 Pokemon HP + active index for each player)
    action_size = 5  # Action space size (2 moves + 3 switch actions)

    agents = {
        "player_0": DQNAgent(state_size, action_size),
        "player_1": DQNAgent(state_size, action_size),
    }

    # Training metrics
    episode_rewards = {"player_0": [], "player_1": []}
    recent_rewards = {"player_0": deque(maxlen=100), "player_1": deque(maxlen=100)}

    # Create save directory
    os.makedirs("models", exist_ok=True)

    for episode in range(episodes):
        env.reset()
        episode_reward = {"player_0": 0, "player_1": 0}
        states = {}

        # Initial observations
        for agent_name in env.agents:
            states[agent_name] = env.observe(agent_name)

        done = False
        step_count = 0
        max_steps = 200  # Prevent infinite loops

        while not done and step_count < max_steps:
            # Current agent takes action
            agent_name = env.agent_selection

            if agent_name in env.agents:
                state = env.observe(agent_name)
                action = agents[agent_name].act(state, training=True)

                # Store previous cumulative reward
                prev_reward = env._cumulative_rewards.get(agent_name, 0)

                # Take action
                env.step(action)

                # Calculate reward (change in cumulative reward)
                reward = env._cumulative_rewards.get(agent_name, 0) - prev_reward
                episode_reward[agent_name] += int(reward) if isinstance(reward, float) else reward

                # Get next state
                next_state = env.observe(agent_name)

                # Check if episode is done
                done = env.terminations.get(agent_name, False)

                # Store transition
                agents[agent_name].remember(state, action, reward, next_state, done)

                # Train the agent
                if len(agents[agent_name].memory) > agents[agent_name].batch_size:
                    agents[agent_name].replay()

            step_count += 1

            # Check if all agents are done
            if all(env.terminations.values()):
                done = True

        # Record episode rewards
        for agent_name in ["player_0", "player_1"]:
            episode_rewards[agent_name].append(episode_reward[agent_name])
            recent_rewards[agent_name].append(episode_reward[agent_name])

        # Update target networks periodically
        if episode % 10 == 0:
            for agent in agents.values():
                agent.update_target_network()

        # Print progress
        if episode % 10 == 0:
            avg_reward_0 = (
                np.mean(recent_rewards["player_0"]) if recent_rewards["player_0"] else 0
            )
            avg_reward_1 = (
                np.mean(recent_rewards["player_1"]) if recent_rewards["player_1"] else 0
            )
            print(f"Episode {episode}/{episodes}")
            print(
                f"  Player 0 - Avg Reward: {avg_reward_0:.3f}, Epsilon: {agents['player_0'].epsilon:.3f}"
            )
            print(
                f"  Player 1 - Avg Reward: {avg_reward_1:.3f}, Epsilon: {agents['player_1'].epsilon:.3f}"
            )
            print(f"  Steps: {step_count}")

        # Save models
        if episode % save_interval == 0 and episode > 0:
            for agent_name, agent in agents.items():
                agent.save(f"models/{agent_name}_episode_{episode}.pt")
            print(f"Models saved at episode {episode}")

    # Final save
    for agent_name, agent in agents.items():
        agent.save(f"models/{agent_name}_final.pt")

    # Plot training progress
    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.plot(episode_rewards["player_0"], alpha=0.5, label="Player 0")
    plt.plot(episode_rewards["player_1"], alpha=0.5, label="Player 1")
    plt.xlabel("Episode")
    plt.ylabel("Episode Reward")
    plt.title("Training Rewards")
    plt.legend()

    plt.subplot(1, 2, 2)
    window = 100
    if len(episode_rewards["player_0"]) >= window:
        avg_rewards_0 = np.convolve(
            episode_rewards["player_0"], np.ones(window) / window, mode="valid"
        )
        avg_rewards_1 = np.convolve(
            episode_rewards["player_1"], np.ones(window) / window, mode="valid"
        )
        plt.plot(avg_rewards_0, label="Player 0 (100-ep avg)")
        plt.plot(avg_rewards_1, label="Player 1 (100-ep avg)")
        plt.xlabel("Episode")
        plt.ylabel("Average Reward")
        plt.title(f"Moving Average Rewards (window={window})")
        plt.legend()

    plt.tight_layout()
    plt.savefig("training_progress.png")
    plt.close()

    return agents


def evaluate_agents(agents, num_games=100, render=False):
    env = PokemonBattleEnv(render_mode="human" if render else None)

    wins = {"player_0": 0, "player_1": 0}

    for game in range(num_games):
        env.reset()
        done = False
        step_count = 0
        max_steps = 200

        while not done and step_count < max_steps:
            agent_name = env.agent_selection

            if agent_name in env.agents:
                state = env.observe(agent_name)
                action = agents[agent_name].act(state, training=False)
                env.step(action)

                if render and game == 0:  # Only render first game
                    env.render()

            step_count += 1

            if all(env.terminations.values()):
                done = True
                # Determine winner based on rewards
                if (
                    env._cumulative_rewards["player_0"]
                    > env._cumulative_rewards["player_1"]
                ):
                    wins["player_0"] += 1
                else:
                    wins["player_1"] += 1

    print(f"\nEvaluation Results ({num_games} games):")
    print(
        f"Player 0 wins: {wins['player_0']} ({wins['player_0'] / num_games * 100:.1f}%)"
    )
    print(
        f"Player 1 wins: {wins['player_1']} ({wins['player_1'] / num_games * 100:.1f}%)"
    )


if __name__ == "__main__":
    print("Starting Pokemon Battle DQN Training...")

    # Train agents
    trained_agents = train_pokemon_dqn(episodes=1000)

    print("\nTraining complete! Evaluating agents...")

    # Evaluate trained agents
    evaluate_agents(trained_agents, num_games=100, render=True)
