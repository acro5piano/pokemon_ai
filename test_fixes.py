#!/usr/bin/env python3
"""
Simple test to verify fainted Pokemon fixes without external dependencies
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
pettingzoo_mock = type('MockPettingZoo', (), {'AECEnv': object})()
utils_mock = type('MockUtils', (), {})()
agent_selector_mock = type('MockAgentSelectorModule', (), {'agent_selector': MockAgentSelector})()

utils_mock.agent_selector = agent_selector_mock
pettingzoo_mock.utils = utils_mock

sys.modules['pettingzoo'] = pettingzoo_mock
sys.modules['pettingzoo.utils'] = utils_mock  
sys.modules['pettingzoo.utils.agent_selector'] = agent_selector_mock

# Now import our battle environment
from pokemon_battle_env import PokemonBattleEnv

def test_fainted_pokemon_fixes():
    """Test that fainted Pokemon bugs are fixed"""
    print("Testing fainted Pokemon fixes...")
    
    env = PokemonBattleEnv()
    env.reset()
    
    # Test 1: Fainted Pokemon cannot attack
    print("\nTest 1: Fainted Pokemon cannot attack")
    
    # Manually set player_0's active Pokemon as fainted
    env.game_state["player_0"]["fainted"][0] = True
    env.game_state["player_0"]["hp"][0] = 0
    
    # Try to make player_0 attack (should be converted to switch)
    original_action = 0  # Attack
    env.step(original_action)
    
    # Check that action was converted to switch (action 2)
    stored_action = env.game_state["actions"].get("player_0")
    if stored_action == 2:
        print("✓ Fainted Pokemon attack converted to switch")
    else:
        print("✗ Fainted Pokemon attack not properly handled")
    
    # Test 2: Cannot switch to fainted Pokemon
    print("\nTest 2: Cannot switch to fainted Pokemon")
    
    # Reset and set up scenario
    env.reset()
    env.game_state["player_0"]["fainted"][1] = True  # Zapdos fainted
    env.game_state["player_0"]["hp"][1] = 0
    
    # Try to switch to fainted Pokemon
    original_active = env.game_state["player_0"]["active"]
    env.step(2)  # Switch action
    env.step(0)  # Player 1 action to trigger resolution
    
    # Check that active Pokemon didn't change to fainted one
    new_active = env.game_state["player_0"]["active"]
    if new_active == original_active:
        print("✓ Switch to fainted Pokemon prevented")
    else:
        print("✗ Switch to fainted Pokemon was allowed")
    
    # Test 3: HP set to 0 when Pokemon faints
    print("\nTest 3: HP properly set to 0 when Pokemon faints")
    
    # Reset and deal exact lethal damage
    env.reset()
    
    # Manually set HP to 1 and apply 1 damage
    env.game_state["player_1"]["hp"][0] = 1
    
    # Player 0 attacks
    env.step(0)  # Attack
    env.step(0)  # Player 1 attacks too
    
    # Check if Pokemon with 0 HP is marked as fainted
    if (env.game_state["player_1"]["hp"][0] == 0 and 
        env.game_state["player_1"]["fainted"][0]):
        print("✓ HP set to 0 and Pokemon marked as fainted")
    else:
        print("✗ HP or faint status not properly handled")
    
    # Test 4: Force switch when Pokemon faints
    print("\nTest 4: Force switch when active Pokemon faints")
    
    # Reset
    env.reset()
    
    # Set active Pokemon as fainted
    env.game_state["player_0"]["fainted"][0] = True
    env.game_state["player_0"]["hp"][0] = 0
    
    # Try to attack (should be forced to switch)
    env.step(0)  # Try to attack
    
    action = env.game_state["actions"].get("player_0")
    if action == 2:
        print("✓ Forced switch when active Pokemon fainted")
    else:
        print("✗ Did not force switch when active Pokemon fainted")
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    test_fainted_pokemon_fixes()