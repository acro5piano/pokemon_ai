from dataclasses import dataclass

from pokemon_ai.simulator.player import Action


@dataclass
class Experience:
    state: list[int]
    action: Action
    reward: float
    next_state: list[int]
    done: bool
