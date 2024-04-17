from enum import Enum


class Action(Enum):
    MOVE_0 = 0
    MOVE_1 = 1

    def is_move(self) -> bool:
        return True

    # TODO: change it later
    # CHANGE_TO_0 = 2
    # CHANGE_TO_1 = 3

    # MOVE_2 = 2
    # MOVE_3 = 3
    # CHANGE_TO_0 = 4
    # CHANGE_TO_1 = 5
    # CHANGE_TO_2 = 6
    # CHANGE_TO_3 = 7
    # CHANGE_TO_4 = 8
    # CHANGE_TO_5 = 9
