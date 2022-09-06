import pokemon_ai.simulator.typechart as t


class Move:
    id: int
    bp: int  # base power
    acc: int  # accuracy
    pp: int  # power points
    type: t.Type  # type

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"


class Earthquake(Move):
    id = 1
    bp = 100
    acc = 100
    pp = 16
    type = t.Ground()


class Surf(Move):
    id = 2
    bp = 95
    acc = 100
    pp = 24
    type = t.Water()


class Thunderbolt(Move):
    id = 3
    bp = 95
    acc = 100
    pp = 24
    type = t.Electric()


class BodySlam(Move):
    id = 4
    bp = 85
    acc = 100
    pp = 24
    type = t.Normal()


class RockSlide(Move):
    id = 5
    bp = 75
    acc = 90
    pp = 16
    type = t.Rock()


class Blizzard(Move):
    id = 6
    bp = 120
    acc = 90
    pp = 8
    type = t.Ice()


class DoubleKick(Move):
    id = 7
    bp = 60
    acc = 100
    pp = 48
    type = t.Fighting()


class PinMissle(Move):
    id = 8
    bp = 42
    acc = 85
    pp = 32
    type = t.Bug()


class Psychic(Move):
    id = 9
    bp = 90
    acc = 100
    pp = 16
    type = t.Psychic()
