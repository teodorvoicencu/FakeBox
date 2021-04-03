import random
import string
from enum import IntEnum

from models.player import Player


class State(IntEnum):
    INACTIVE = 0
    AWAITING_VIP = 1
    AWAITING_PLAYERS = 2
    ACTIVE = 3


class GameException(RuntimeError):
    pass


class Game:
    def __init__(self):
        self.player_count = 0
        self.code = self.generate_code(4)
        self.players = {}
        # Game logic before activation: put pieces on a board or smth...
        self.state = State.AWAITING_VIP

    def add_player(self, nickname, websocket, is_vip=False):
        player = Player(nickname, websocket, is_vip)

        self.players[self.player_count] = player
        player.player_id = self.player_count

        if is_vip:
            if self.state == State.AWAITING_VIP:
                self.state = State.AWAITING_PLAYERS
            else:
                raise GameException("Game already has a VIP.")

        self.player_count += 1

        return player

    def get_player(self, uuid):
        return self.players.get(uuid, None)

    def start_game(self):
        self.state = State.ACTIVE

    @property
    def has_started(self):
        return self.state == State.ACTIVE

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
