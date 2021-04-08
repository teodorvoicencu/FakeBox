import json
import logging

import asyncio
import websockets

from common.actions import Actions
from models.game import Game, State, GameException
from common.handling_exception import HandlingException

logging.basicConfig(level=logging.INFO)

STATE = {}
SHARED_STATE = {}
LOGGER = logging.getLogger('hello')
USERS = set()


def get_game():
    return STATE.get("game", None)


def set_game(game):
    STATE["game"] = game


def reject_event(message):
    return json.dumps({
        "action": Actions.PLAYER_REJECTED,
        "message": message,
    })


async def login_handler(websocket, path, data):
    if get_game().state not in [State.AWAITING_VIP, State.AWAITING_PLAYERS]:
        return reject_event("Game is no longer taking in players.")

    code = data.get("code", None)
    if not get_game().code == code:
        return reject_event("Incorrect room code.")

    nickname = data.get("nickname", None)
    if not nickname:
        return reject_event("Empty nickname.")

    player = get_game().add_player(nickname, websocket)

    # Player successfully joined
    LOGGER.info('New player joined. Players: %s.', [player for player in get_game().players.values()])

    return json.dumps({
        "action": Actions.PLAYER_ACCEPTED,
        "player_id": player.player_id,
        "is_vip": player.is_vip,
    })


HANDLERS = {
    Actions.PLAYER_LOGIN: login_handler,
}


async def game(websocket, path):
    if not get_game():
        set_game(Game())
        LOGGER.info("Game code is %s.", get_game().code)

    async for message in websocket:
        data = json.loads(message)
        LOGGER.info("Received event. Data: %s.", data)

        response = None
        can_handle = False
        event_action = data.get("action", None)
        for action, handler in HANDLERS.items():
            if event_action == action.value:
                can_handle = True
                try:
                    response = await handler(websocket, path, data)
                except (GameException, HandlingException) as e:
                    LOGGER.info("Game or handling error: %s", str(e))

        if not can_handle:
            LOGGER.info("Cannot handle action of type '%s'", str(event_action))

        if response:
            await websocket.send(response)


start_server = websockets.serve(game, "localhost", 8765)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
