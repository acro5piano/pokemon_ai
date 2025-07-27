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

        # Action space: 0-1 for moves, 2-4 for switch to Pokemon 0-2
        self._action_spaces = {agent: spaces.Discrete(5) for agent in self.agents}

        # Observation space: [p0_pkmn0_hp, p0_pkmn1_hp, p0_pkmn2_hp, p0_active_idx,
        #                     p1_pkmn0_hp, p1_pkmn1_hp, p1_pkmn2_hp, p1_active_idx]
        self._observation_spaces = {
            agent: spaces.Box(low=0, high=523, shape=(8,), dtype=np.float32)
            for agent in self.agents
        }

        self.render_mode = render_mode

        # Pokemon stats
        self.pokemon_names = ["Snorlax", "Zapdos", "Nidoking"]
        self.pokemon_max_hp = [523, 383, 365]  # [Snorlax, Zapdos, Nidoking]
        self.pokemon_speeds = [30, 100, 85]  # [Snorlax, Zapdos, Nidoking]

        # Damage table
        self.damage_table = {
            # (attacker_idx, defender_idx, move_idx): damage
            # Snorlax attacks
            (0, 0, 0): 166,  # Snorlax vs Snorlax, Return
            (0, 0, 1): 109,  # Snorlax vs Snorlax, Earthquake
            (0, 1, 0): 142,  # Snorlax vs Zapdos, Return
            (0, 1, 1): 0,  # Snorlax vs Zapdos, Earthquake
            (0, 2, 0): 150,  # Snorlax vs Nidoking, Return
            (0, 2, 1): 198,  # Snorlax vs Nidoking, Earthquake
            # Zapdos attacks
            (1, 0, 0): 123,  # Zapdos vs Snorlax, Thunderbolt
            (1, 0, 1): 61,  # Zapdos vs Snorlax, Hidden Power Ice
            (1, 1, 0): 141,  # Zapdos vs Zapdos, Thunderbolt
            (1, 1, 1): 140,  # Zapdos vs Zapdos, Hidden Power Ice
            (1, 2, 0): 0,  # Zapdos vs Nidoking, Thunderbolt
            (1, 2, 1): 155,  # Zapdos vs Nidoking, Hidden Power Ice
            # Nidoking attacks
            (2, 0, 0): 145,  # Nidoking vs Snorlax, Earthquake
            (2, 0, 1): 63,  # Nidoking vs Snorlax, Ice Beam
            (2, 1, 0): 0,  # Nidoking vs Zapdos, Earthquake
            (2, 1, 1): 146,  # Nidoking vs Zapdos, Ice Beam
            (2, 2, 0): 262,  # Nidoking vs Nidoking, Earthquake
            (2, 2, 1): 162,  # Nidoking vs Nidoking, Ice Beam
        }

        self.move_names = {
            0: ["Return", "Earthquake"],
            1: ["Thunderbolt", "Hidden Power Ice"],
            2: ["Earthquake", "Ice Beam"],
        }

        self.game_state: Dict[str, Any] = {}
        self.observations: Dict[str, np.ndarray] = {}
        self.infos: Dict[str, Dict[str, Any]] = {}
        self._cumulative_rewards: Dict[str, float] = {}
        self.rewards: Dict[str, float] = {}
        self.terminations: Dict[str, bool] = {}
        self.truncations: Dict[str, bool] = {}

    def get_observation_space(self, agent):
        return self._observation_spaces[agent]

    def get_action_space(self, agent):
        return self._action_spaces[agent]

    def reset(self, seed=None, options=None):
        self.agents = self.possible_agents[:]
        self._agent_selector = agent_selector(self.agents)
        self.agent_selection = self._agent_selector.next()

        # Initialize game state
        self.game_state = {
            "player_0": {
                "active": 0,  # Snorlax (default active)
                "hp": [
                    self.pokemon_max_hp[0],
                    self.pokemon_max_hp[1],
                    self.pokemon_max_hp[2],
                ],  # [Snorlax, Zapdos, Nidoking]
                "fainted": [False, False, False],
            },
            "player_1": {
                "active": 0,  # Snorlax (default active)
                "hp": [
                    self.pokemon_max_hp[0],
                    self.pokemon_max_hp[1],
                    self.pokemon_max_hp[2],
                ],  # [Snorlax, Zapdos, Nidoking]
                "fainted": [False, False, False],
            },
            "actions": {},  # Store actions for simultaneous resolution
        }

        self.observations = {
            agent: self._get_observation(agent) for agent in self.agents
        }
        self.infos = {agent: {} for agent in self.agents}
        self._cumulative_rewards = {agent: 0 for agent in self.agents}
        self.rewards = {agent: 0 for agent in self.agents}
        self.terminations = {agent: False for agent in self.agents}
        self.truncations = {agent: False for agent in self.agents}

    def _is_valid_switch(self, player_state, target_idx):
        """Check if switching to target_idx is valid"""
        return (
            0 <= target_idx < 3
            and not player_state["fainted"][target_idx]
            and target_idx != player_state["active"]
        )
    
    def get_valid_actions(self, agent):
        """Get list of valid actions for the current agent"""
        if agent not in self.game_state:
            return [0, 1]  # Default to moves only
            
        player_state = self.game_state[agent]
        valid_actions = []
        
        # Moves are always available (0, 1)
        valid_actions.extend([0, 1])
        
        # Add valid switch actions
        for i in range(3):
            if self._is_valid_switch(player_state, i):
                valid_actions.append(2 + i)  # Switch actions are 2, 3, 4
        
        return valid_actions

    def _get_observation(self, agent):
        obs = np.zeros(8, dtype=np.float32)

        if not self.game_state:
            return obs

        # Player 0 stats: HP of all 3 Pokemon + active index
        obs[0] = self.game_state["player_0"]["hp"][0]  # Snorlax HP
        obs[1] = self.game_state["player_0"]["hp"][1]  # Zapdos HP
        obs[2] = self.game_state["player_0"]["hp"][2]  # Nidoking HP
        obs[3] = self.game_state["player_0"]["active"]  # Active Pokemon index

        # Player 1 stats: HP of all 3 Pokemon + active index
        obs[4] = self.game_state["player_1"]["hp"][0]  # Snorlax HP
        obs[5] = self.game_state["player_1"]["hp"][1]  # Zapdos HP
        obs[6] = self.game_state["player_1"]["hp"][2]  # Nidoking HP
        obs[7] = self.game_state["player_1"]["active"]  # Active Pokemon index

        return obs

    def step(self, action):
        if (
            self.terminations[self.agent_selection]
            or self.truncations[self.agent_selection]
        ):
            self._was_dead_step(action)
            return

        agent = self.agent_selection

        # Validate action against current valid actions
        valid_actions = self.get_valid_actions(agent)
        if action not in valid_actions:
            # If invalid action, default to first valid action
            action = valid_actions[0] if valid_actions else 0

        player_state = self.game_state[agent]

        # Handle forced switch if active Pokemon fainted
        if player_state["fainted"][player_state["active"]]:
            if action < 2:  # Must switch
                # Find first valid Pokemon to switch to
                for i in range(3):
                    if self._is_valid_switch(player_state, i):
                        action = 2 + i  # Switch to Pokemon i
                        break
                else:
                    # All Pokemon fainted - this should not happen in valid gameplay
                    pass

        # Reset rewards for this step
        self.rewards = {agent: 0 for agent in self.agents}
        
        # Store action
        self.game_state["actions"][agent] = action

        # If both players have acted, resolve turn
        if len(self.game_state["actions"]) == 2:
            self._resolve_turn()
            self.game_state["actions"] = {}

            # Update observations
            for a in self.agents:
                self.observations[a] = self._get_observation(a)

            # Check for game end
            for agent_check in self.agents:
                if all(self.game_state[agent_check]["fainted"]):
                    self.terminations = {a: True for a in self.agents}
                    # Set final rewards: winner gets +1, loser gets -1
                    for a in self.agents:
                        if a == agent_check:
                            self.rewards[a] = -1  # Loser
                            self._cumulative_rewards[a] += -1
                        else:
                            self.rewards[a] = 1   # Winner
                            self._cumulative_rewards[a] += 1
                    break

        # Move to next agent
        self.agent_selection = self._agent_selector.next()

    def _resolve_turn(self):
        actions = self.game_state["actions"]

        # Handle switches first (switches always go first)
        for agent in self.agents:
            if actions[agent] >= 2:  # Switch action
                player_state = self.game_state[agent]
                target_idx = actions[agent] - 2

                # Only switch if target Pokemon is valid and not fainted
                if self._is_valid_switch(player_state, target_idx):
                    player_state["active"] = target_idx

        # Then handle attacks based on speed priority
        attacking_agents = []
        for agent in self.agents:
            if actions[agent] < 2:  # Attack action
                attacker = self.game_state[agent]
                attacker_idx = attacker["active"]

                # Skip if attacker is fainted
                if not attacker["fainted"][attacker_idx]:
                    speed = self.pokemon_speeds[attacker_idx]
                    attacking_agents.append((agent, speed))

        # Sort by speed (highest first), use agent name as tiebreaker for consistency
        attacking_agents.sort(key=lambda x: (-x[1], x[0]))

        # Execute attacks in speed order
        for agent, _ in attacking_agents:
            attacker = self.game_state[agent]
            attacker_idx = attacker["active"]

            # Check again if attacker is still alive (might have been knocked out)
            if attacker["fainted"][attacker_idx]:
                continue

            defender_agent = "player_1" if agent == "player_0" else "player_0"
            defender = self.game_state[defender_agent]
            defender_idx = defender["active"]

            # Skip attack if defender is already fainted
            if defender["fainted"][defender_idx]:
                continue

            # Get damage
            move_idx = actions[agent]
            damage = self.damage_table.get((attacker_idx, defender_idx, move_idx), 0)

            # Apply damage
            defender["hp"][defender_idx] = max(0, defender["hp"][defender_idx] - damage)

            # Check for faint - set HP to exactly 0 and mark as fainted
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
                player = self.game_state[agent]
                active_idx = player["active"]

                for pokemon_idx in range(3):
                    pokemon_name = self.pokemon_names[pokemon_idx]
                    max_hp = self.pokemon_max_hp[pokemon_idx]
                    current_hp = player["hp"][pokemon_idx]
                    status = (
                        " (ACTIVE)"
                        if pokemon_idx == active_idx
                        else " (FAINTED)"
                        if player["fainted"][pokemon_idx]
                        else ""
                    )

                    print(f"  {pokemon_name}: {current_hp}/{max_hp} HP{status}")

            print("\n" + "=" * 50)

    def observation_space(self, agent):
        return self._observation_spaces[agent]

    def action_space(self, agent):
        return self._action_spaces[agent]
    
    def get_action_mask(self, agent):
        """Get action mask for valid actions (1 for valid, 0 for invalid)"""
        if agent not in self.game_state:
            return [1, 1, 1, 1, 1]  # All actions valid initially
            
        valid_actions = self.get_valid_actions(agent)
        mask = [0] * 5  # Initialize all as invalid
        for action in valid_actions:
            mask[action] = 1  # Mark valid actions
        
        return mask
