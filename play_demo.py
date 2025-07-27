import os

import numpy as np

from dqn_agent import DQNAgent
from pokemon_battle_env import PokemonBattleEnv


def play_against_ai(agent_path=None):
    env = PokemonBattleEnv(render_mode="human")

    # Load trained agent for player 1
    ai_agent = DQNAgent(state_size=8, action_size=5)
    if agent_path and os.path.exists(agent_path):
        try:
            ai_agent.load(agent_path)
            ai_agent.epsilon = 0  # No exploration during play
            print(f"Loaded AI agent from {agent_path}")
        except Exception as e:
            print(f"Warning: Could not load agent from {agent_path}: {e}")
            print("Using untrained AI agent with new architecture")
    else:
        print("Using untrained AI agent")

    print("\n=== POKEMON BATTLE DEMO ===")
    print("You are Player 0 with Snorlax (active), Zapdos, and Nidoking")
    print("\nActions:")
    print("0: Use Move 1 (Snorlax: Return, Zapdos: Thunderbolt, Nidoking: Earthquake)")
    print("1: Use Move 2 (Snorlax: Earthquake, Zapdos: Hidden Power Ice, Nidoking: Ice Beam)")
    print("2: Switch to Snorlax")
    print("3: Switch to Zapdos")
    print("4: Switch to Nidoking\n")

    env.reset()
    done = False

    while not done:
        env.render()
        agent_name = env.agent_selection

        if agent_name == "player_0":
            # Human player
            while True:
                try:
                    action = int(input(f"\n{agent_name} - Choose action (0-4): "))
                    if 0 <= action <= 4:
                        break
                    else:
                        print("Invalid action! Choose 0-4.")
                except ValueError:
                    print("Invalid input! Enter a number.")
        else:
            # AI player
            state = env.observe(agent_name)
            action = ai_agent.act(state, training=False)
            print(f"\n{agent_name} (AI) chose action: {action}")

        env.step(action)

        if all(env.terminations.values()):
            done = True

    env.render()

    # Determine winner
    if env._cumulative_rewards["player_0"] > env._cumulative_rewards["player_1"]:
        print("\n🎉 YOU WIN! 🎉")
    else:
        print("\n💀 YOU LOSE! 💀")

    print(
        f"\nFinal rewards - Player 0: {env._cumulative_rewards['player_0']}, "
        f"Player 1: {env._cumulative_rewards['player_1']}"
    )


def watch_ai_battle(agent1_path=None, agent2_path=None):
    env = PokemonBattleEnv(render_mode="human")

    # Load agents
    agents = {}
    for i, (agent_name, path) in enumerate(
        [("player_0", agent1_path), ("player_1", agent2_path)]
    ):
        agents[agent_name] = DQNAgent(state_size=8, action_size=5)
        if path and os.path.exists(path):
            try:
                agents[agent_name].load(path)
                agents[agent_name].epsilon = 0
                print(f"Loaded {agent_name} from {path}")
            except Exception as e:
                print(f"Warning: Could not load {agent_name} from {path}: {e}")
                print(f"Using untrained agent for {agent_name}")
        else:
            print(f"Using untrained agent for {agent_name}")

    print("\n=== AI vs AI BATTLE ===")
    input("Press Enter to start...")

    env.reset()
    done = False
    step = 0

    while not done and step < 200:
        env.render()
        agent_name = env.agent_selection

        if agent_name in env.agents:
            state = env.observe(agent_name)
            action = agents[agent_name].act(state, training=False)

            move_names = {
                0: ["Return", "Earthquake"],
                1: ["Thunderbolt", "Hidden Power Ice"],
                2: ["Earthquake", "Ice Beam"],
            }

            if action < 2:
                active_idx = env.game_state[agent_name]["active"]
                move_name = move_names[active_idx][action]
                print(f"\n{agent_name} uses {move_name}!")
            else:
                pokemon_names = ["Snorlax", "Zapdos", "Nidoking"]
                target_idx = action - 2
                print(f"\n{agent_name} switches to {pokemon_names[target_idx]}!")

            env.step(action)

            input("Press Enter to continue...")

        step += 1

        if all(env.terminations.values()):
            done = True

    env.render()

    if env._cumulative_rewards["player_0"] > env._cumulative_rewards["player_1"]:
        print("\n🏆 PLAYER 0 WINS! 🏆")
    else:
        print("\n🏆 PLAYER 1 WINS! 🏆")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "watch":
        # Watch AI vs AI
        agent1 = (
            "models/player_0_final.pt"
            if os.path.exists("models/player_0_final.pt")
            else None
        )
        agent2 = (
            "models/player_1_final.pt"
            if os.path.exists("models/player_1_final.pt")
            else None
        )
        watch_ai_battle(agent1, agent2)
    else:
        # Play against AI
        agent_path = (
            "models/player_1_final.pt"
            if os.path.exists("models/player_1_final.pt")
            else None
        )
        play_against_ai(agent_path)
