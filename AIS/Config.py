from utils import *


class Config:

    _config: dict = {}

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(Config, cls).__new__(cls, *args, **kwargs)

        if bool(Config._config) is False:
            Config._readConfig()
        return cls.instance

    @staticmethod
    def _readConfig() -> dict:
        print("Reading credentials")
        Config._config = {}
        with open(f"{CONFIG_FILE}", mode="rb") as f:
            config_dict: dict = load(f)
            Config._config["API_KEY"]: str = config_dict[WORK_ENV]["api"]["secret_key"]
            Config._config["GH_USERNAME"]: str = config_dict[WORK_ENV]["gh"]["username"]
            Config._config["GH_PASSWORD"]: str = config_dict[WORK_ENV]["gh"]["password"]
        return Config._config

    @staticmethod
    def getConfig() -> dict:
        print("Getting credentials")
        return Config._config if bool(Config._config) is False else Config._readConfig()
