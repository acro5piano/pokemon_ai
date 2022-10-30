from math import floor

import pokemon_ai.simulator.moves as m
import pokemon_ai.simulator.typechart as t
from pokemon_ai.simulator.constant import LEVEL, MAX_DETERMINANT_VALUE


def calculate_actual_hp(hp: int):
    return (
        floor(
            ((hp + MAX_DETERMINANT_VALUE) * 2 + min(63, floor(floor(1 + 65535) / 4))) * LEVEL / 100
        )
        + LEVEL
        + 10
    )


class Pokemon:
    id: int
    types: list[t.Type]
    hp: int
    atk: int
    def_: int
    spa: int
    spd: int
    spe: int
    available_moves: list[m.Move]

    actual_hp: int
    actual_moves: list[m.Move]

    def __init__(self, moves: list[m.Move] = []):
        self.actual_hp = calculate_actual_hp(self.hp)
        self.actual_moves = moves

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.actual_hp})"

    def to_array(self):
        return [
            self.id,
            self.actual_hp,
            *[m.id for m in self.actual_moves],
        ]


class Rhydon(Pokemon):
    id = 112
    types = [t.Ground(), t.Rock()]
    hp = 105
    atk = 130
    def_ = 120
    spa = 45
    spd = 45
    spe = 40
    available_moves = []


class Starmie(Pokemon):
    id = 121
    types = [t.Water(), t.Psychic()]
    hp = 60
    atk = 75
    def_ = 85
    spa = 100
    spd = 100
    spe = 115
    available_moves = []


class Jolteon(Pokemon):
    id = 135
    types = [t.Electric()]
    hp = 65
    atk = 65
    def_ = 60
    spa = 110
    spd = 110
    spe = 130
    available_moves = []
