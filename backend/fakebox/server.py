import json
import logging

import asyncio
import websockets

from common.message_types import MessageTypes
from models.game import Game, State, GameException
from models.player import Player

logging.basicConfig(level=logging.INFO)

STATE = {}
SHARED_STATE = {}
LOGGER = logging.getLogger('hello')
USERS = set()


def get_game():
    return STATE.get("game", None)


def set_game(game):
    STATE["game"] = game


# def state_event():
#     return json.dumps({"type": "state", **SHARED_STATE})
#
#
# def users_event():
#     return json.dumps({"type": "users", "count": len(USERS)})
#
#
# async def notify_state():
#     if USERS:
#         message = state_event()
#         await asyncio.wait([user.send(message) for user in USERS])
#
#
# async def notify_users():
#     if USERS:
#         message = users_event()
#         await asyncio.wait([user.send(message) for user in USERS])


def login_response_event(player):
    return json.dumps({
        "action": "login_response",
        "player_id": player.player_id,
        "is_vip": player.is_vip,
    })


async def register(websocket, player_data):
    try:
        player = get_game().add_player(
            player_data["nickname"],
            websocket,
            is_vip=(False if get_game().has_vip else True),
        )

        await websocket.send(login_response_event(player))
    except GameException:
        LOGGER.error("Bad message.")


async def unregister(websocket):
    USERS.remove(websocket)
    # await notify_users()


async def game(websocket, path):
    if not get_game():
        set_game(Game())
        LOGGER.info("Game code is %s.", get_game().code)

    async for message in websocket:
        data = json.loads(message)
        LOGGER.info("Received event. Data: %s.", data)
        if data["action"] == "login":
            await register(websocket, data)
        else:
            LOGGER.error("Unsupported event: %s.", data["action"])
    # finally:
    # await unregister(websocket)


start_server = websockets.serve(game, "localhost", 8765)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
