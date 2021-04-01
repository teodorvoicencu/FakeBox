import json

import asyncio
import websockets

from common.message_types import MessageTypes

STATE = {}


def set_id(uuid: str):
    STATE["player_uuid"] = uuid


def get_id() -> str:
    return STATE.get("player_uuid", None)


async def hello():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        name = input("Set a nickname: ")

        await websocket.send(name)

        server_response = await websocket.recv()
        parsed_response = json.loads(server_response)

        message_type = MessageTypes(int(parsed_response["type"]))
        uuid = str(parsed_response["id"])

        set_id(uuid)
        is_vip = True if message_type == MessageTypes.SUCCESSFUL_VIP_LOGIN else False
        STATE["is_vip"] = is_vip

        print(f"This player's UUID is {uuid} and VIP status is {is_vip}.")

        while True:
            command = input(">")
            if command == "exit":
                return


asyncio.get_event_loop().run_until_complete(hello())
