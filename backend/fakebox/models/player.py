import uuid


class Player:
    def __init__(self, nickname: str, is_vip: bool = False):
        self.uuid = uuid.uuid4()
        self.nickname = nickname
        self.is_vip = is_vip
