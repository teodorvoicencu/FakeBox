import random
import string
from enum import IntEnum


class State(IntEnum):
    INACTIVE = 0
    AWAITING_VIP = 1
    AWAITING_PLAYERS = 2
    ACTIVE = 3


class GameException(RuntimeError):
    pass


class Game:
    def __init__(self):
        self.code = self.generate_code(4)
        self.players = {}
        # Game logic before activation: put pieces on a board or smth...
        self.state = State.AWAITING_VIP

    def set_vip(self, vip_player):
        if self.state != State.AWAITING_VIP:
            return GameException("Game already has a VIP.")

        self.add_player(vip_player)
        self.state = State.AWAITING_PLAYERS

    def add_player(self, player):
        uuid = player.uuid
        self.players[uuid] = player

    def start_game(self):
        self.state = State.ACTIVE

    def await_players(self):
        pass

    def step(self):
        pass

    def cleanup(self):
        pass

    @property
    def has_vip(self):
        """Whether the initial player has joined."""
        if len(self.players) == 0:
            return False

        return any(player.is_vip for player in self.players.values())

    @staticmethod
    def generate_code(k):
        return ''.join(random.choices(string.ascii_uppercase, k=k))
