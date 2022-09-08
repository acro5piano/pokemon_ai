from dataclasses import dataclass

from pokemon_ai.simulator.player import Action


@dataclass
class Experience:
    state: list[float]
    action: Action
    reward: float
    next_state: list[float]
    done: bool
