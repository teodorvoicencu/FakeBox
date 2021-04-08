from enum import auto, IntEnum


class Actions(IntEnum):
    PLAYER_LOGIN = auto()
    PLAYER_ACCEPTED = auto()
    PLAYER_REJECTED = auto()
