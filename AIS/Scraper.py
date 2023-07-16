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
    subscribe_message_json = json.dumps(subscribe_message)
    try:
        async with websockets.connect(uri=f"{API_BASE_URL}") as websocket:
            await websocket.send(subscribe_message_json)
            async for message_json in websocket:
                message = json.loads(message_json)
                print(message)
    except ConnectionResetError as e:
        print(f"ConnectionError: {e}")
    except Exception as e:
        print(f"Error: {e}")
