import websockets
from tomli import load
from .constants import *
import json
import asyncio


with open(f"{CONFIG_FILE}", mode="rb") as f:
    config_dict: dict = load(f)
    API_KEY: str = config_dict[WORK_ENV]["api"]["secret_key"]


async def connect_ais_stream(m):
    async with websockets.connect(uri=f"{API_BASE_URL}") as websocket:
        subscribe_message = {
            "APIKey": f"{API_KEY}",
            "BoundingBoxes": [[[-90, -180], [90, 180]]]
        }
        subscribe_message_json = json.dumps(subscribe_message)
        await websocket.send(subscribe_message_json)
        async for message_json in websocket:
            message = json.loads(message_json)
            print(message)
            m.append(message)

"""
TODO
    - Add a feature to retrieve Usage (open Issue)
"""