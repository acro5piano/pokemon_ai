#!/usr/bin/env python3
"""
Test suite for the expanded 3-Pokemon battle system
"""

import sys
import os

# Mock numpy array functionality for testing
class MockArray:
    def __init__(self, data):
        self.data = data
        self.shape = (len(data),)
    
    def __getitem__(self, idx):
        return self.data[idx]
    
    def __setitem__(self, idx, value):
        self.data[idx] = value

# Mock numpy module
class MockNumpy:
    float32 = float
    
    @staticmethod
    def zeros(size, dtype=None):
        return MockArray([0.0] * size)

# Mock spaces module
class MockSpaces:
    class Discrete:
        def __init__(self, n):
            self.n = n
    
    class Box:
        def __init__(self, low, high, shape, dtype):
            self.shape = shape
            self.dtype = dtype

# Mock agent selector
class MockAgentSelector:
    def __init__(self, agents):
        self.agents = agents
        self.current = 0
    
    def next(self):
        agent = self.agents[self.current]
        self.current = (self.current + 1) % len(self.agents)
        return agent

# Insert mocks into sys.modules
sys.modules['numpy'] = MockNumpy()
sys.modules['gymnasium'] = type('MockGymnasium', (), {'spaces': MockSpaces()})()

# Create a more complete pettingzoo mock
from typing import Any

class MockPettingZoo:
    AECEnv = object
    
    def __init__(self):
        self.utils: Any = None

class MockUtils:
    def __init__(self):
        self.agent_selector: Any = None

class MockAgentSelectorModule:
    agent_selector = MockAgentSelector

pettingzoo_mock = MockPettingZoo()
utils_mock = MockUtils()
agent_selector_mock = MockAgentSelectorModule()

utils_mock.agent_selector = agent_selector_mock
pettingzoo_mock.utils = utils_mock

sys.modules['pettingzoo'] = pettingzoo_mock
sys.modules['pettingzoo.utils'] = utils_mock  
sys.modules['pettingzoo.utils.agent_selector'] = agent_selector_mock

# Now import our battle environment
from pokemon_battle_env import PokemonBattleEnv

def test_3pokemon_initialization():
    """Test that 3-Pokemon system initializes correctly"""
    print("Testing 3-Pokemon initialization...")
    
    env = PokemonBattleEnv()
    env.reset()
    
    # Test Pokemon stats
    print("\nTest 1: Pokemon stats verification")
    expected_names = ["Snorlax", "Zapdos", "Nidoking"]
    expected_hp = [523, 383, 365]
    expected_speeds = [30, 100, 85]
    
    if (env.pokemon_names == expected_names and 
        env.pokemon_max_hp == expected_hp and
        env.pokemon_speeds == expected_speeds):
        print("✓ Pokemon stats correctly configured")
    else:
        print("✗ Pokemon stats incorrect")
        print(f"  Names: {env.pokemon_names}")
        print(f"  HP: {env.pokemon_max_hp}")
        print(f"  Speeds: {env.pokemon_speeds}")
    
    # Test action space
    print("\nTest 2: Action space verification")
    if env.action_space("player_0").n == 5:
        print("✓ Action space correctly expanded to 5 actions")
    else:
        print(f"✗ Action space wrong size: {env.action_space('player_0').n}")
    
    # Test observation space
    print("\nTest 3: Observation space verification")
    if env.observation_space("player_0").shape == (8,):
        print("✓ Observation space correctly expanded to 8 dimensions")
    else:
        print(f"✗ Observation space wrong size: {env.observation_space('player_0').shape}")
    
    # Test game state
    print("\nTest 4: Game state verification")
    player_0 = env.game_state["player_0"]
    if (len(player_0["hp"]) == 3 and 
        len(player_0["fainted"]) == 3 and
        player_0["hp"] == [523, 383, 365]):
        print("✓ Game state correctly initialized for 3 Pokemon")
    else:
        print("✗ Game state incorrect")
        print(f"  HP: {player_0['hp']}")
        print(f"  Fainted: {player_0['fainted']}")

def test_3pokemon_switching():
    """Test switching between 3 Pokemon"""
    print("\n" + "="*50)
    print("Testing 3-Pokemon switching...")
    
    env = PokemonBattleEnv()
    env.reset()
    
    # Test 1: Switch to Zapdos (action 3)
    print("\nTest 1: Switch to Zapdos")
    initial_active = env.game_state["player_0"]["active"]
    env.step(3)  # Switch to Pokemon 1 (Zapdos)
    env.step(0)  # Player 1 action
    
    new_active = env.game_state["player_0"]["active"]
    if new_active == 1:
        print("✓ Successfully switched to Zapdos")
    else:
        print(f"✗ Switch failed. Active: {new_active}, expected: 1")
    
    # Test 2: Switch to Nidoking (action 4)
    print("\nTest 2: Switch to Nidoking")
    env.step(4)  # Switch to Pokemon 2 (Nidoking)
    env.step(0)  # Player 1 action
    
    new_active = env.game_state["player_0"]["active"]
    if new_active == 2:
        print("✓ Successfully switched to Nidoking")
    else:
        print(f"✗ Switch failed. Active: {new_active}, expected: 2")
    
    # Test 3: Invalid switch (to same Pokemon)
    print("\nTest 3: Invalid switch to same Pokemon")
    env.step(4)  # Try to switch to Nidoking again
    env.step(0)  # Player 1 action
    
    # Should stay as Nidoking since invalid switch converts to move
    if env.game_state["player_0"]["active"] == 2:
        print("✓ Invalid switch properly handled")
    else:
        print("✗ Invalid switch not handled correctly")

def test_3pokemon_damage():
    """Test damage calculations with 3 Pokemon"""
    print("\n" + "="*50)
    print("Testing 3-Pokemon damage...")
    
    env = PokemonBattleEnv()
    env.reset()
    
    # Test 1: Snorlax vs Nidoking damage
    print("\nTest 1: Snorlax Return vs Nidoking")
    env.game_state["player_1"]["active"] = 2  # Set player 1 to Nidoking
    
    initial_hp = env.game_state["player_1"]["hp"][2]
    env.step(0)  # Player 0 Snorlax uses Return
    env.step(0)  # Player 1 Nidoking uses Earthquake
    
    damage_dealt = initial_hp - env.game_state["player_1"]["hp"][2]
    expected_damage = 150  # Snorlax Return vs Nidoking
    
    if damage_dealt == expected_damage:
        print(f"✓ Correct damage: {damage_dealt}")
    else:
        print(f"✗ Wrong damage: {damage_dealt}, expected: {expected_damage}")
    
    # Test 2: Nidoking vs Snorlax (damage from previous turn)
    print("\nTest 2: Nidoking Earthquake vs Snorlax")
    # The damage was already applied in the previous turn resolution
    final_p0_hp = env.game_state["player_0"]["hp"][0]
    damage_from_nidoking = 523 - final_p0_hp  # Initial HP - current HP
    expected_damage = 145  # Nidoking Earthquake vs Snorlax
    
    if damage_from_nidoking == expected_damage:
        print(f"✓ Correct damage: {damage_from_nidoking}")
    else:
        print(f"✗ Wrong damage: {damage_from_nidoking}, expected: {expected_damage}")

def test_3pokemon_speed_order():
    """Test speed-based turn order with 3 Pokemon"""
    print("\n" + "="*50)
    print("Testing 3-Pokemon speed order...")
    
    env = PokemonBattleEnv()
    env.reset()
    
    # Test speed stats
    print("\nTest 1: Speed stats verification")
    speeds = {
        "Snorlax": env.pokemon_speeds[0],
        "Zapdos": env.pokemon_speeds[1], 
        "Nidoking": env.pokemon_speeds[2]
    }
    
    print(f"  Snorlax: {speeds['Snorlax']}")
    print(f"  Zapdos: {speeds['Zapdos']}")
    print(f"  Nidoking: {speeds['Nidoking']}")
    
    # Verify speed order: Zapdos > Nidoking > Snorlax
    if speeds["Zapdos"] > speeds["Nidoking"] > speeds["Snorlax"]:
        print("✓ Speed order correct: Zapdos > Nidoking > Snorlax")
    else:
        print("✗ Speed order incorrect")

def test_3pokemon_faint_handling():
    """Test fainting with 3 Pokemon"""
    print("\n" + "="*50)
    print("Testing 3-Pokemon faint handling...")
    
    env = PokemonBattleEnv()
    env.reset()
    
    # Test 1: Faint current Pokemon, should force switch
    print("\nTest 1: Force switch when active Pokemon faints")
    env.game_state["player_0"]["hp"][0] = 0  # Faint Snorlax
    env.game_state["player_0"]["fainted"][0] = True
    
    env.step(0)  # Try to attack (should be converted to switch)
    stored_action = env.game_state["actions"].get("player_0")
    
    if stored_action >= 2:  # Should be a switch action
        print("✓ Forced switch when Pokemon fainted")
    else:
        print(f"✗ No forced switch. Action: {stored_action}")
    
    # Test 2: Cannot switch to fainted Pokemon
    print("\nTest 2: Cannot switch to fainted Pokemon")
    env.reset()
    env.game_state["player_0"]["fainted"][1] = True  # Faint Zapdos
    
    env.step(3)  # Try to switch to fainted Zapdos
    env.step(0)  # Player 1 action
    
    # Should still be Snorlax since Zapdos is fainted
    if env.game_state["player_0"]["active"] == 0:
        print("✓ Cannot switch to fainted Pokemon")
    else:
        print("✗ Switch to fainted Pokemon was allowed")

def test_observation_structure():
    """Test observation structure for 3 Pokemon"""
    print("\n" + "="*50)
    print("Testing observation structure...")
    
    env = PokemonBattleEnv()
    env.reset()
    
    obs = env.observe("player_0")
    
    print(f"Observation: {obs.data}")
    print("Expected structure:")
    print("  [0-2]: Player 0 Pokemon HP (Snorlax, Zapdos, Nidoking)")
    print("  [3]: Player 0 active Pokemon index")
    print("  [4-6]: Player 1 Pokemon HP (Snorlax, Zapdos, Nidoking)")
    print("  [7]: Player 1 active Pokemon index")
    
    # Verify observation values
    expected = [523, 383, 365, 0, 523, 383, 365, 0]
    if obs.data == expected:
        print("✓ Observation structure correct")
    else:
        print("✗ Observation structure incorrect")
        print(f"  Got: {obs.data}")
        print(f"  Expected: {expected}")

if __name__ == "__main__":
    test_3pokemon_initialization()
    test_3pokemon_switching()
    test_3pokemon_damage()
    test_3pokemon_speed_order()
    test_3pokemon_faint_handling()
    test_observation_structure()
    print("\n" + "="*50)
    print("All 3-Pokemon tests completed!")