import logging as log
from datetime import datetime

import yaml as yaml


class DiaryConfig:
    __config_path = "config.yml"
    dir_path: str = None
    first_use: bool = None
    log_time_format: str = None
    owner_credentials_file_name: str = None
    date_format: str = None
    natural_date_format: str = None
    data_extension: str = None
    __keys = []

    @classmethod
    def load(cls, config_path = "./"):
        with open(config_path + cls.__config_path, mode="r") as f:
            cfg = yaml.safe_load(f)
        if not cfg:
            raise RuntimeError("Cannot find config file.")

        cls.__keys = cfg.keys()

        try:
            cls.dir_path = cfg['dir_path']
            cls.first_use = cfg["first_use"]
            cls.log_time_format = cfg['log_time_format']
            cls.owner_credentials_file_name = cfg["owner_credentials_file_name"]
            cls.date_format = cfg["date_format"]
            cls.natural_date_format = cfg["natural_date_format"]
            cls.data_extension = cfg["data_extension"]
        except KeyError as ke:
            log.error(datetime.now().strftime("%d.%m.%Y-%H:%M:%S") + f" - Unknown error in config file. {ke}")
            raise RuntimeError(f"Config file has been corrupted. {ke}")

    @classmethod
    def save(cls):
        cfg = {key: value for key, value in cls.__dict__.items() if key in cls.__keys}
        try:
            with open(cls.__config_path, "w") as f:
                yaml.safe_dump(data=cfg, stream=f)
        except IOError as e:
            log.error(datetime.now().strftime(cls.log_time_format) + f" - Error writing to config.yml file. {e}")
            raise e
