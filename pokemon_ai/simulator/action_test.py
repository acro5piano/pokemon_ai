from pokemon_ai.simulator.action import Action


def action_test():
    a = Action.MOVE_0
    assert a.is_move() == True
