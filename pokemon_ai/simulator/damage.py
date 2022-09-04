from math import floor
from random import randint, random

from pokemon_ai.logger import log
from pokemon_ai.simulator.constant import LEVEL, MAX_DETERMINANT_VALUE
from pokemon_ai.simulator.moves import Move
from pokemon_ai.simulator.pokedex import Pokemon


def to_real_value(stat: int) -> int:
    return (
        floor(
            ((stat + MAX_DETERMINANT_VALUE) * 2 + min(63, floor(floor(1 + 65535) / 4)))
            * LEVEL
            / 100
        )
        + 5
    )


def calculate_damage(attacker: Pokemon, defender: Pokemon, move: Move) -> int:
    is_critical_hit = random() < (attacker.spe / 512)
    if is_critical_hit:
        log("a critical hit!")

    modifier = 1

    for defender_type in defender.types:
        for regist in defender_type.regists:
            if regist == move.type.__class__.__name__:
                modifier *= 0.5
        for weak_to in defender_type.weak_to:
            if weak_to == move.type.__class__.__name__:
                modifier *= 2
        for immune_to in defender_type.immune_to:
            if immune_to == move.type.__class__.__name__:
                modifier = 0

    if modifier > 1:
        log(f"super effective! {modifier}")
    if modifier < 1:
        log(f"It's not very effective... {modifier}")

    for attacker_type in attacker.types:
        if attacker_type == move.type:
            modifier *= 1.5
            log("STAB attack!")

    modifier *= randint(217, 255) / 255

    # TODO:
    # - status changes (amnesia, screech, etc.)
    # - 1/256 miss
    # - reflect/light screen

    real_atk = to_real_value(attacker.atk if move.type.is_physical else attacker.spa)
    real_def = to_real_value(defender.def_ if move.type.is_physical else defender.spd)
    real_level = LEVEL * 2 if is_critical_hit else LEVEL

    damage = floor(
        floor(floor(floor(real_level * 2 / 5 + 2) * move.bp * real_atk / real_def) / 50 + 2)
        * modifier
    )

    if damage > defender.actual_hp:
        return defender.actual_hp
    else:
        return damage
