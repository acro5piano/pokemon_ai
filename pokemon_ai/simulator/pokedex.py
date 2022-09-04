from math import floor

import pokemon_ai.simulator.typechart as t
from pokemon_ai.simulator.constant import LEVEL, MAX_DETERMINANT_VALUE


class Pokemon:
    types: list[t.Type]
    hp: int
    atk: int
    def_: int
    spa: int
    spd: int
    spe: int
    actual_hp: int

    def __init__(self):
        self.actual_hp = (
            floor(
                ((self.hp + MAX_DETERMINANT_VALUE) * 2 + min(63, floor(floor(1 + 65535) / 4)))
                * LEVEL
                / 100
            )
            + LEVEL
            + 10
        )


class Rhydon(Pokemon):
    types = [t.Ground(), t.Rock()]
    hp = 105
    atk = 130
    def_ = 120
    spa = 45
    spd = 45
    spe = 40


class Starmie(Pokemon):
    types = [t.Water(), t.Psychic()]
    hp = 60
    atk = 75
    def_ = 85
    spa = 100
    spd = 100
    spe = 115


class Jolteon(Pokemon):
    types = [t.Electric()]
    hp = 65
    atk = 65
    def_ = 60
    spa = 110
    spd = 110
    spe = 130
