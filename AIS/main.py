import websockets
from tomli import load
from .constants import *


with open(f"{CONFIG_FILE}", mode="rb") as f:
    config_dict: dict = load(f)

    API_KEY: str = config_dict[WORK_ENV]["api"]["secret_key"]
