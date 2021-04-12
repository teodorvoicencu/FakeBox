import json
import logging
from dataclasses import dataclass
from typing import Callable

import asyncio
import websockets

from common.actions import Actions

from common.handling_exception import HandlingException

logging.basicConfig(level=logging.INFO)
STATE = {}
URI = "ws://localhost:8765"


def set_id(uuid: int):
    STATE["player_id"] = uuid


def get_id() -> str:
    return STATE.get("player_id", None)


class CommandException(RuntimeError):
    pass


async def join_command(websocket, arguments):
    game_code = str(arguments[0])
    nickname = str(arguments[1])

    await websocket.send(json.dumps({
        "action": Actions.PLAYER_LOGIN.value,
        "nickname": nickname,
        "code": game_code,
    }))


@dataclass
class Command:
    name: str
    argument_count: int
    command: Callable


COMMANDS = {
    "join": Command("join", 2, join_command),
    # "start": start_game_command,
    # "exit": exit_command
}


async def ui_logic():
    logger = logging.getLogger('ui')
    async with websockets.connect(URI) as websocket:
        while True:
            user_input = input("?>")
            parsed_input = user_input.split()
            command_name, arguments = parsed_input[0], parsed_input[1:]

            if command_name not in COMMANDS:
                logger.info("Command '%s' not recognized.", command_name)

            command = COMMANDS[command_name]
            if len(arguments) != command.argument_count:
                logger.info("'%s' takes %d arguments.", command_name, command.argument_count)

            try:
                await command.command(websocket, arguments)
            except CommandException as e:
                logger.info("Could not run '%s': %s", command_name, str(e))

            # Yield to the other coroutine
            await asyncio.sleep(0)


async def accepted_handler(websocket, logger, data):
    STATE["player_id"] = int(data["player_id"])
    STATE["is_vip"] = data["is_vip"]
    logger.info("This player's ID is {} and VIP status is {}.".format(STATE["player_id"], STATE["is_vip"]))


async def rejected_handler(websocket, logger, data):
    rejection_message = data.get("message", "<Could not retrieve message>")
    logger.info(f"Rejected login with message: {rejection_message}.")


HANDLERS = {
    Actions.PLAYER_ACCEPTED: accepted_handler,
    Actions.PLAYER_REJECTED: rejected_handler,
}


async def event_handler():
    logger = logging.getLogger('event_handler')
    async with websockets.connect(URI) as websocket:
        async for message in websocket:
            data = json.loads(message)
            logger.info("Received event. Data: %s.", data)

            response = None
            can_handle = False
            event_action = data.get("action", None)
            for action, handler in HANDLERS.items():
                if event_action == action.value:
                    can_handle = True
                    try:
                        response = await handler(websocket, logger, data)
                    except HandlingException as e:
                        logger.info("Game or handling error: %s", str(e))

            if not can_handle:
                logger.info("Cannot handle action of type '%s'", str(event_action))

            if response:
                await websocket.send(response)

            # Yield to the other coroutine
            await asyncio.sleep(0)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(ui_logic())
        loop.run_until_complete(event_handler())
        loop.run_forever()
    finally:
        loop.close()
