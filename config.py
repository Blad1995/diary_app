import logging as log
from datetime import datetime

import yaml as yaml


class DiaryConfig:
    def __init__(self):
        with open("config.yml", mode="r") as f:
            self.cfg = yaml.safe_load(f)
        if not self.cfg:
            raise RuntimeError("Cannot find config file.")

        try:
            self.dir_path = self.cfg['diary']['dir_path']
            self.log_time_format = self.cfg['general']['log_time_format']
            self.owner_login_file_name = self.cfg["diary"]["owner_login_file_name"]
            self.first_use = self.cfg["general"]["first_use"]
        except KeyError as ke:
            log.error(datetime.now().strftime("%d.%m.%Y-%H:%M:%S") + f" - Unknown error in config file. {ke}")
            raise RuntimeError(f"Config file has been corrupted. {ke}")
