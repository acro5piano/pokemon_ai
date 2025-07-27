import os

import numpy as np

from dqn_agent import DQNAgent
from pokemon_battle_env import PokemonBattleEnv


def play_against_ai(agent_path=None):
    env = PokemonBattleEnv(render_mode="human")

    # Load trained agent for player 1
    ai_agent = DQNAgent(state_size=6, action_size=3)
    if agent_path and os.path.exists(agent_path):
        ai_agent.load(agent_path)
        ai_agent.epsilon = 0  # No exploration during play
        print(f"Loaded AI agent from {agent_path}")
    else:
        print("Using untrained AI agent")

    print("\n=== POKEMON BATTLE DEMO ===")
    print("You are Player 0 with Snorlax (active) and Zapdos (bench)")
    print("\nActions:")
    print("0: Use Move 1 (Snorlax: Return, Zapdos: Thunderbolt)")
    print("1: Use Move 2 (Snorlax: Earthquake, Zapdos: Hidden Power Ice)")
    print("2: Switch Pokemon\n")

    env.reset()
    done = False

    while not done:
        env.render()
        agent_name = env.agent_selection

        if agent_name == "player_0":
            # Human player
            while True:
                try:
                    action = int(input(f"\n{agent_name} - Choose action (0-2): "))
                    if 0 <= action <= 2:
                        break
                    else:
                        print("Invalid action! Choose 0, 1, or 2.")
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
        agents[agent_name] = DQNAgent(state_size=6, action_size=3)
        if path and os.path.exists(path):
            agents[agent_name].load(path)
            agents[agent_name].epsilon = 0
            print(f"Loaded {agent_name} from {path}")
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
            }

            if action < 2:
                active_idx = env.state[agent_name]["active"]
                move_name = move_names[active_idx][action]
                print(f"\n{agent_name} uses {move_name}!")
            else:
                print(f"\n{agent_name} switches Pokemon!")

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
