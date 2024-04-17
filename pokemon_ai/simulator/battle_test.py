import random

from pokemon_ai.simulator.action import Action
from pokemon_ai.simulator.battle import Battle, BattleResult
from pokemon_ai.simulator.dex import BodySlam, Snorlax
from pokemon_ai.simulator.player import Player

random.seed(42)


def test_battle():
    player1 = Player([Snorlax()])
    player2 = Player([Snorlax()])
    battle = Battle(player1, player2)
    assert battle.calculate_damage(Snorlax(), Snorlax(), BodySlam()) == 138
    assert battle.forward_step(Action.MOVE_0, Action.MOVE_0) == None
    assert player1.active_pokemon().hp == (523 - 138)
    assert player2.active_pokemon().hp == (523 - 138)
    assert battle.forward_step(Action.MOVE_0, Action.MOVE_1) == None
    assert player1.active_pokemon().hp == (523 - 138 - 109)
    assert player2.active_pokemon().hp == (523 - 138 - 138)
    assert battle.forward_step(Action.MOVE_1, Action.MOVE_0) == None
    assert player1.active_pokemon().hp == (523 - 138 - 109 - 138)
    assert player2.active_pokemon().hp == (523 - 138 - 138 - 109)
    assert battle.forward_step(Action.MOVE_0, Action.MOVE_0) == BattleResult.PLAYER1_WON
