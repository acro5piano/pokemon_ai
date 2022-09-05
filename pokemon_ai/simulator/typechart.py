# TODO: use class instead of str
from __future__ import annotations


class Type:
    id: int
    is_physical: bool
    weak_to: list[str] = []
    regists: list[str] = []
    immune_to: list[str] = []

    def __eq__(self, other):
        return self.__class__.__name__ == other.__class__.__name__


class Bug(Type):
    id = 1
    is_physical = True
    weak_to = ["Fire", "Flying", "Rock"]
    regists = ["Grass", "Fighting", "Ground"]


class Dragon(Type):
    id = 2
    is_physical = False
    weak_to = ["Ice", "Dragon", "Fairy"]
    regists = ["Fire", "Water", "Grass", "Electric"]


class Electric(Type):
    id = 3
    is_physical = False
    weak_to = ["Ground"]
    regists = ["Electric", "Flying", "Steel"]


class Flying(Type):
    id = 4
    is_physical = True
    weak_to = ["Electric", "Ice", "Rock"]
    regists = ["Grass", "Fighting", "Bug"]
    immune_to = ["Ground"]


class Fighting(Type):
    id = 5
    is_physical = True
    weak_to = ["Flying", "Psychic", "Fairy"]
    regists = ["Bug", "Rock", "Dark"]


class Fire(Type):
    id = 6
    is_physical = False
    weak_to = ["Water", "Ground", "Rock"]
    regists = ["Fire", "Grass", "Ice", "Bug", "Steel", "Fairy"]


class Grass(Type):
    id = 7
    is_physical = False
    weak_to = ["Fire", "Ice", "Poison", "Flying", "Bug"]
    regists = ["Water", "Grass", "Electric", "Ground"]


class Ghost(Type):
    id = 8
    is_physical = True
    weak_to = ["Ghost", "Dark"]
    regists = ["Poison", "Bug"]
    immune_to = ["Normal", "Fighting"]


class Ground(Type):
    id = 9
    is_physical = True
    weak_to = ["Water", "Grass", "Ice"]
    regists = ["Poison", "Rock"]
    immune_to = ["Electric"]


class Ice(Type):
    id = 10
    is_physical = False
    weak_to = ["Fire", "Fighting", "Rock", "Steel"]
    regists = ["Ice"]


class Normal(Type):
    id = 11
    is_physical = True
    weak_to = ["Fighting"]
    regists = []
    immune_to = ["Ghost"]


class Rock(Type):
    id = 12
    is_physical = True
    weak_to = ["Water", "Grass", "Fighting", "Ground", "Steel"]
    regists = ["Normal", "Fire", "Poison", "Flying"]


class Poison(Type):
    id = 13
    is_physical = True
    weak_to = ["Ground", "Psychic"]
    regists = ["Grass", "Fighting", "Poison", "Bug", "Fairy"]


class Psychic(Type):
    id = 14
    is_physical = False
    regists = ["Fighting", "Psychic"]
    immune_to = ["Ghost"]


class Water(Type):
    id = 15
    is_physical = False
    weak_to = ["Grass", "Electric"]
    regists = ["Fire", "Water", "Ice", "Steel"]
