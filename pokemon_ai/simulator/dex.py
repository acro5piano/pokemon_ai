class Move:
    power: int


class BodySlam(Move):
    power = 85


class Thunder(Move):
    power = 120


class Pokemon:
    hp: int
    spe: int
    move1: Move

    def get_move(self, index: int) -> Move:
        match index:
            case 1:
                return self.move1
            case _:
                raise NotImplementedError


class Zapdos(Pokemon):
    hp = 383
    spe = 100
    move1 = Thunder()
    # move2 = "Hidden Power Ice"


class Snorlax(Pokemon):
    hp = 523
    spe = 30
    move1 = BodySlam()
    # move2 = "Earthquake"
