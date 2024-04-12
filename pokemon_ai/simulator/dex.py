class Move:
    power: int


class BodySlam(Move):
    power = 85


class Thunder(Move):
    power = 120


class Earthquake(Move):
    power = 100


class Pokemon:
    hp: int
    spe: int
    move0: Move
    move1: Move

    # def get_move_by_action(self, action: Action) -> Move:
    #     match action:
    #         case Action.MOVE_0:
    #             return self.move0
    #         case Action.MOVE_1:
    #             return self.move1
    #         case _:
    #             raise NotImplementedError


class Zapdos(Pokemon):
    hp = 383
    spe = 100
    move0 = Thunder()
    # move1 = "Hidden Power Ice"


class Snorlax(Pokemon):
    hp = 523
    spe = 30
    move0 = BodySlam()
    move1 = Earthquake()
