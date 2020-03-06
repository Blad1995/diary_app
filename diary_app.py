# @Ondřej Divina & Jan Melichařík

import logging as log
import os as os
import pickle as pickle
from datetime import datetime

from config import DiaryConfig
# my modules
from diary_owner import Owner


class DiaryApp:
    cfg = DiaryConfig

    def __init__(self):
        self.owners = []
        self.active_owner = None

    def save_data_to_disc(self):
        # check path where to store data from config file
        # make directory if needed
        if not os.path.isdir(DiaryApp.cfg.dir_path):
            os.mkdir(DiaryApp.cfg.dir_path)
        self.set_config_first_use_false()
        owners_logins = [o.login for o in self.owners]
        # Saves every Owner separately
        for o_index, login in enumerate(owners_logins):
            owner_file_path = DiaryApp.cfg.dir_path + login + ".Ddata"
            try:
                with open(owner_file_path, mode="wb") as f:
                    pickle.dump(obj=self.owners[o_index], file=f, protocol=pickle.HIGHEST_PROTOCOL)
            except IOError as e:
                log.error(datetime.now().strftime(DiaryApp.cfg.log_time_format) + f"Error writing to {owner_file_path} file. {e}")
                raise RuntimeError(f"Can't open the file {owner_file_path} to save data.")

        try:
            owner_path = DiaryApp.cfg.dir_path + DiaryApp.cfg.owner_login_file_name
        except KeyError as e:
            log.error(datetime.now().strftime(DiaryApp.cfg.log_time_format) + "Cannot locate 'diary:owner_login_file_name' in config file")
            raise RuntimeError("Config file has been corrupted. 'diary:owner_login_file_name' missing.")

        try:
            # Saves owners login to file
            with open(owner_path, mode="wb") as f:
                pickle.dump(obj=owners_logins, file=f, protocol=pickle.HIGHEST_PROTOCOL)
        except IOError as e:
            log.error(datetime.now().strftime(DiaryApp.cfg.log_time_format) + f"Error writing to {owner_path} file. {e}")
            raise RuntimeError(f"Can't open the file {owner_path} to save data.")

    def load_all_data_from_disc(self):
        try:
            # tries to find Owner logins file path in config file
            owner_path = DiaryApp.cfg.dir_path + DiaryApp.cfg.owner_login_file_name
        except KeyError as e:
            log.error(datetime.now().strftime(DiaryApp.cfg.log_time_format) + "Cannot locate 'diary:owner_login_file_name' in config file")
            raise RuntimeError("Config file has been corrupted. 'diary:owner_login_file_name' missing.")

        # try to read the owner logins from file
        try:
            with open(owner_path, mode="rb") as f:
                owners_logins = pickle.load(f)
        except FileNotFoundError as e:
            log.error(datetime.now().strftime(DiaryApp.cfg.log_time_format) + f"File {owner_path} not found")
            raise RuntimeError(f"File {owner_path} not found. Can't load the data.")
        except IOError as e:
            log.error(datetime.now().strftime(DiaryApp.cfg.log_time_format) + f"Error reading {owner_path} file. {e}")
            raise RuntimeError(f"Can't load the data from {owner_path}.")

        # load all data about owners
        # FIXME do budoucna možná bude potřeba předělat na samostatné načítání po jednom Ownerovi -->
        #  paměťové nároky na načtení všech dat vs jednoho Ownera
        for o_index, login in enumerate(owners_logins):
            owner_file_path = DiaryApp.cfg.dir_path + login + ".Ddata"
            try:
                with open(owner_file_path, mode="rb") as f:
                    new_owner = pickle.load(file=f)
                    self.owners.append(new_owner)
            except IOError as e:
                log.error(datetime.now().strftime(DiaryApp.cfg.log_time_format) + f"Error writing to {owner_path} file. {e}")
                raise RuntimeError(f"Can't open the file {owner_file_path} to save data.")

    @classmethod
    def set_config_first_use_false(cls):
        # No exception should occur. This property of cfg was already addressed.
        cls.cfg.first_use = False
        cls.cfg.save()


if __name__ == "__main__":
    app_config = DiaryConfig
    app_config.load()
    main_app = DiaryApp()
    if main_app.cfg.first_use:
        print("First use was used")
        main_app.owners.append(Owner(login="Blad", password="Heslo století"))

        main_app.save_data_to_disc()
    else:
        main_app.load_all_data_from_disc()
    print(main_app)

    app_config.save()
