from utils import *


class Config:

    _config: dict = {}

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(Config, cls).__new__(cls, *args, **kwargs)
        if bool(Config._config) is False:
            Config._readConfig(work_env_=WorkEnv.LOCAL)
        return cls.instance

    @staticmethod
    def _readConfig(work_env_: str = WorkEnv.LOCAL) -> dict:
        print("Reading credentials")
        with open(f"{CONFIG_FILE}", mode="rb") as f:
            config_dict: dict = load(f)
            try:
                Config._config["API_KEY"]: str = config_dict[work_env_]["api"]["secret_key"]
                Config._config["GH_USERNAME"]: str = config_dict[work_env_]["gh"]["username"]
                Config._config["GH_PASSWORD"]: str = config_dict[work_env_]["gh"]["password"]
            except KeyError as e:
                print(f"Error: {e}")
                return {}
        return Config._config

    @staticmethod
    def getConfig(work_env: str = WorkEnv.LOCAL) -> dict:
        print("Getting credentials")
        return Config._config if bool(Config._config) is True else Config._readConfig(work_env_=work_env)
