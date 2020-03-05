import logging as log
from datetime import datetime

import yaml as yaml


class DiaryConfig:
    # TODO předávání confogu při načítání z disku
    def __init__(self):
        with open("config.yml", mode="r") as f:
            self.cfg = yaml.safe_load(f)
        if not self.cfg:
            raise RuntimeError("Cannot find config file.")

        try:
            self.__dir_path = self.cfg['diary']['dir_path']
            self.__first_use = self.cfg["general"]["first_use"]
            self.__log_time_format = self.cfg['general']['log_time_format']
            self.__owner_login_file_name = self.cfg["diary"]["owner_login_file_name"]
        except KeyError as ke:
            log.error(datetime.now().strftime("%d.%m.%Y-%H:%M:%S") + f" - Unknown error in config file. {ke}")
            raise RuntimeError(f"Config file has been corrupted. {ke}")

    @property
    def dir_path(self):
        return self.__dir_path

    @dir_path.setter
    def dir_path(self, new_dir_path):
        self.__dir_path = new_dir_path
        self.cfg.update({"dir_path": new_dir_path})

    @property
    def first_use(self):
        return self.__first_use

    @first_use.setter
    def first_use(self, new_first_use):
        self.cfg["general"].update({"first_use": new_first_use})
        print(self.cfg)
        self.__first_use = new_first_use

    @property
    def log_time_format(self):
        return self.__log_time_format

    @log_time_format.setter
    def log_time_format(self, new_log_time_format):
        self.__log_time_format = new_log_time_format
        self.cfg.update({"log_time_format": new_log_time_format})

    @property
    def owner_login_file_name(self):
        return self.__owner_login_file_name

    @owner_login_file_name.setter
    def owner_login_file_name(self, new_owner_login_file_name):
        self.__owner_login_file_name = new_owner_login_file_name
        self.cfg.update({"owner_login_file_name": new_owner_login_file_name})

    def save_config_to_disc(self):
        try:
            with open("config.yml", "w") as f:
                print(f)
                yaml.safe_dump(data=self.cfg, stream=f)
        except IOError as e:
            log.error(datetime.now().strftime(self.cfg.log_time_format) + f"Error writing to config.yml file. {e}")
            raise e
