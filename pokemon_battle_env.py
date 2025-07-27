import functools
from typing import Any, Dict, Optional, Tuple

import numpy as np
from gymnasium import spaces
from pettingzoo import AECEnv
from pettingzoo.utils.agent_selector import agent_selector


class PokemonBattleEnv(AECEnv):
    metadata = {"render_modes": ["human"], "name": "pokemon_battle_v0"}

    def __init__(self, render_mode=None):
        super().__init__()

        self.possible_agents = ["player_0", "player_1"]
        self.agents = self.possible_agents[:]
        self.agent_name_mapping = dict(
            zip(self.possible_agents, range(len(self.possible_agents)))
        )

        self._agent_selector = agent_selector(self.agents)
        self.agent_selection = self._agent_selector.next()

        # Action space: 0-1 for moves, 2 for switch
        self._action_spaces = {agent: spaces.Discrete(3) for agent in self.agents}

        # Observation space: [p0_active_hp, p0_bench_hp, p0_active_idx,
        #                     p1_active_hp, p1_bench_hp, p1_active_idx]
        self._observation_spaces = {
            agent: spaces.Box(low=0, high=523, shape=(6,), dtype=np.float32)
            for agent in self.agents
        }

        self.render_mode = render_mode

        # Pokemon stats
        self.max_hp = 523
        self.pokemon_names = ["Snorlax", "Zapdos"]

        # Damage table
        self.damage_table = {
            # (attacker_idx, defender_idx, move_idx): damage
            (0, 0, 0): 166,  # Snorlax vs Snorlax, Return
            (0, 0, 1): 109,  # Snorlax vs Snorlax, Earthquake
            (0, 1, 0): 142,  # Snorlax vs Zapdos, Return
            (0, 1, 1): 0,  # Snorlax vs Zapdos, Earthquake
            (1, 0, 0): 123,  # Zapdos vs Snorlax, Thunderbolt
            (1, 0, 1): 61,  # Zapdos vs Snorlax, Hidden Power Ice
            (1, 1, 0): 141,  # Zapdos vs Zapdos, Thunderbolt
            (1, 1, 1): 140,  # Zapdos vs Zapdos, Hidden Power Ice
        }

        self.move_names = {
            0: ["Return", "Earthquake"],
            1: ["Thunderbolt", "Hidden Power Ice"],
        }

        self.state = None
        self.observations = None
        self.infos = None
        self._cumulative_rewards = None
        self.terminations = None
        self.truncations = None

    def observation_space(self, agent):
        return self._observation_spaces[agent]

    def action_space(self, agent):
        return self._action_spaces[agent]

    def reset(self, seed=None, options=None):
        self.agents = self.possible_agents[:]
        self._agent_selector = agent_selector(self.agents)
        self.agent_selection = self._agent_selector.next()

        # Initialize game state
        self.state = {
            "player_0": {
                "active": 0,  # Snorlax
                "hp": [self.max_hp, self.max_hp],  # [Snorlax, Zapdos]
                "fainted": [False, False],
            },
            "player_1": {
                "active": 0,  # Snorlax
                "hp": [self.max_hp, self.max_hp],  # [Snorlax, Zapdos]
                "fainted": [False, False],
            },
            "actions": {},  # Store actions for simultaneous resolution
        }

        self.observations = {
            agent: self._get_observation(agent) for agent in self.agents
        }
        self.infos = {agent: {} for agent in self.agents}
        self._cumulative_rewards = {agent: 0 for agent in self.agents}
        self.terminations = {agent: False for agent in self.agents}
        self.truncations = {agent: False for agent in self.agents}

    def _get_observation(self, agent):
        obs = np.zeros(6, dtype=np.float32)

        # Player 0 stats
        obs[0] = self.state["player_0"]["hp"][self.state["player_0"]["active"]]
        bench_idx = 1 - self.state["player_0"]["active"]
        obs[1] = self.state["player_0"]["hp"][bench_idx]
        obs[2] = self.state["player_0"]["active"]

        # Player 1 stats
        obs[3] = self.state["player_1"]["hp"][self.state["player_1"]["active"]]
        bench_idx = 1 - self.state["player_1"]["active"]
        obs[4] = self.state["player_1"]["hp"][bench_idx]
        obs[5] = self.state["player_1"]["active"]

        return obs

    def step(self, action):
        if (
            self.terminations[self.agent_selection]
            or self.truncations[self.agent_selection]
        ):
            self._was_dead_step(action)
            return

        agent = self.agent_selection

        # Validate action
        if action not in range(3):
            action = 0

        # Handle forced switch if active Pokemon fainted
        player_state = self.state[agent]
        if player_state["fainted"][player_state["active"]]:
            if action != 2:  # Must switch
                action = 2

        # Store action
        self.state["actions"][agent] = action

        # If both players have acted, resolve turn
        if len(self.state["actions"]) == 2:
            self._resolve_turn()
            self.state["actions"] = {}

            # Update observations
            for a in self.agents:
                self.observations[a] = self._get_observation(a)

            # Check for game end
            for agent in self.agents:
                if all(self.state[agent]["fainted"]):
                    self.terminations = {a: True for a in self.agents}
                    # Rewards: winner gets +1, loser gets -1
                    for a in self.agents:
                        if a == agent:
                            self._cumulative_rewards[a] = -1
                        else:
                            self._cumulative_rewards[a] = 1

        # Move to next agent
        self.agent_selection = self._agent_selector.next()

    def _resolve_turn(self):
        actions = self.state["actions"]

        # Handle switches first
        for agent in self.agents:
            if actions[agent] == 2:  # Switch
                player_state = self.state[agent]
                player_state["active"] = 1 - player_state["active"]

        # Then handle attacks
        for agent in self.agents:
            if actions[agent] < 2:  # Attack
                attacker = self.state[agent]
                defender_agent = "player_1" if agent == "player_0" else "player_0"
                defender = self.state[defender_agent]

                # Get damage
                attacker_idx = attacker["active"]
                defender_idx = defender["active"]
                move_idx = actions[agent]

                damage = self.damage_table.get(
                    (attacker_idx, defender_idx, move_idx), 0
                )

                # Apply damage
                defender["hp"][defender_idx] = max(
                    0, defender["hp"][defender_idx] - damage
                )

                # Check for faint
                if defender["hp"][defender_idx] == 0:
                    defender["fainted"][defender_idx] = True

    def observe(self, agent):
        return self.observations[agent]

    def render(self):
        if self.render_mode == "human":
            print("\n" + "=" * 50)
            print("POKEMON BATTLE STATUS")
            print("=" * 50)

            for i, agent in enumerate(["player_0", "player_1"]):
                print(f"\n{agent.upper()}:")
                player = self.state[agent]
                active_idx = player["active"]
                active_name = self.pokemon_names[active_idx]

                print(
                    f"  Active: {active_name} (HP: {player['hp'][active_idx]}/{self.max_hp})"
                )

                bench_idx = 1 - active_idx
                bench_name = self.pokemon_names[bench_idx]
                print(
                    f"  Bench: {bench_name} (HP: {player['hp'][bench_idx]}/{self.max_hp})"
                )

            print("\n" + "=" * 50)

    @functools.lru_cache(maxsize=None)
    def observation_space(self, agent):
        return self._observation_spaces[agent]

    @functools.lru_cache(maxsize=None)
    def action_space(self, agent):
        return self._action_spaces[agent]
