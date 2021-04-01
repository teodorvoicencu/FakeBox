import json
import logging

import asyncio
import websockets

from common.message_types import MessageTypes
from models.game import Game
from models.player import Player

logging.basicConfig(level=logging.INFO)

STATE = {}
LOGGER = logging.getLogger('hello')


def get_game():
    return STATE.get("game", None)


def set_game(game):
    STATE["game"] = game


async def vip_joins(websocket):
    nickname = await websocket.recv()

    LOGGER.info("Initiating game with VIP '%s'.", nickname)

    if not get_game().has_vip:
        vip_player = Player(nickname, is_vip=True)
        get_game().set_vip(vip_player)

        await websocket.send(
            json.dumps(
                {
                    "type": MessageTypes.SUCCESSFUL_VIP_LOGIN.value,
                    "id": str(vip_player.uuid),
                }
            )
        )
    else:
        await handle_regular_player(websocket, nickname)


async def players_join(websocket):
    game = get_game()

    # Incoming messages can either be players
    # requesting to join or the VIP player
    # requesting to start the game.
    message = await websocket.recv()
    message = json.loads(message)

    if message.type == MessageTypes.VIP_PRESSED_START:
        game.start()
    else:
        await handle_regular_player(websocket, message.name)


async def handle_regular_player(websocket, nickname):
    player = Player(nickname)
    get_game().add_player(player)

    await websocket.send(
        json.dumps(
            {
                "type": MessageTypes.SUCCESSFUL_LOGIN.value,
                "id": str(player.uuid),
            }
        )
    )


async def main(websocket, path):
    if not get_game():
        game = Game()
        set_game(game)
        LOGGER.info("Game created.")

    LOGGER.info("Welcome to room %s.", get_game().code)

    if not get_game().has_vip:
        await vip_joins(websocket)

    LOGGER.info("Awaiting for other players to join.")

    await players_join(websocket)


start_server = websockets.serve(main, "localhost", 8765)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
