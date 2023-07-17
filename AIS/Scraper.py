import datetime
import json

from .utils import *
from .Config import *


class Scraper:
    def __init__(self) -> None:
        pass

    def __del__(self) -> None:
        pass

    def startScraping(self):
        pass


async def connect_ais_stream():
    API_KEY: str = Config.getConfig()['API_KEY']
    subscribe_message = {
        "APIKey": f"{API_KEY}",
        "BoundingBoxes": [[[-90, -180], [90, 180]]]
    }
    handshake_msg = json.dumps(subscribe_message)
    f = open(f"../out/messages/msg_{datetime.datetime.now().isoformat()}.dat", "w")
    try:
        async with websockets.connect(uri=f"{API_BASE_URL}") as websocket:
            await websocket.send(handshake_msg)

            async for message_json in websocket:
                message = json.loads(message_json)
                f.write(json.dumps(message))
                print(time.time_ns(), message)
    except KeyboardInterrupt as e:
        f.close()
    except ConnectionResetError as e:
        print(f"ConnectionError: {e}")
    except Exception as e:
        print(f"Error: {e}")
