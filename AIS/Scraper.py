from .utils import *


async def connect_ais_stream():
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
