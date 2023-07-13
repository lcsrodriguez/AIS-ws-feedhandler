import websockets
from tomli import load
from constants import *
import os
import glob
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
import matplotlib.dates as mdates
import datetime
import pickle

with open(f"{CONFIG_FILE}", mode="rb") as f:
    config_dict: dict = load(f)
    API_KEY: str = config_dict[WORK_ENV]["api"]["secret_key"]
    GH_USERNAME: str = config_dict[WORK_ENV]["gh"]["username"]
    GH_PASSWORD: str = config_dict[WORK_ENV]["gh"]["password"]