class Player:
    def __init__(self, player_id: int, nickname: str, websocket, is_vip: bool = False):
        self.player_id = player_id
        self.nickname = nickname
        self.is_vip = is_vip
        self.websocket = websocket
