import pokemon_ai.simulator.typechart as t


class Move:
    bp: int  # base power
    acc: int  # accuracy
    pp: int  # power points
    type: t.Type  # type

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"


class Earthquake(Move):
    bp = 100
    acc = 100
    pp = 16
    type = t.Ground()


class Surf(Move):
    bp = 95
    acc = 100
    pp = 24
    type = t.Water()


class Thunderbolt(Move):
    bp = 95
    acc = 100
    pp = 24
    type = t.Electric()
