import json

import asyncio
import websockets

STATE = {}


def set_id(uuid: int):
    STATE["player_id"] = uuid


def get_id() -> str:
    return STATE.get("player_id", None)


def login_request(name):
    return json.dumps({
        "action": "login", "nickname": name,
    })


async def hello():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        name = input("Set a nickname: ")
        await websocket.send(login_request(name))

        message = await websocket.recv()
        data = json.loads(message)

        if data["action"] == "login_response":
            STATE["player_id"] = int(data["player_id"])
            STATE["is_vip"] = data["is_vip"]
            print("This player's UUID is {} and VIP status is {}.".format(
                STATE["player_id"], STATE["is_vip"]
            ))

        # while True:
        #     command = input(">")
        #     if command == "exit":
        #         return
        #
        #     if command == "start":
        #         await websocket.send(json.dumps({
        #             "type": MessageTypes.VIP_PRESSES_START.value,
        #             "id": uuid,
        #         }))


asyncio.get_event_loop().run_until_complete(hello())
