import websockets
from tomli import load
from .constants import *
import json
import asyncio
from typing import List
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options
from operator import itemgetter
import pandas as pd
import matplotlib.pyplot as plt

with open(f"{CONFIG_FILE}", mode="rb") as f:
    config_dict: dict = load(f)
    API_KEY: str = config_dict[WORK_ENV]["api"]["secret_key"]
    GH_USERNAME: str = config_dict[WORK_ENV]["gh"]["username"]
    GH_PASSWORD: str = config_dict[WORK_ENV]["gh"]["password"]


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
