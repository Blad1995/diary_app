# @Ondřej Divina & Jan Melichařík

import logging as log
import os as os
import pickle as pickle
from datetime import datetime

# my modules
from backend_scripts.diary_owner import Owner
from config import DiaryConfig


class DiaryApp:
    """
    Controls whole app Diary. Contains methods for storing and loading data from files and stores all owners and other data.
    """
    cfg = DiaryConfig  # :class variable for storing loaded config file.

    def __init__(self):
        """
        Initialize empty class.
        """
        self.__owners = []  # Contains all owners of the diaries.
        self.__active_owner_id = None  # Variable for storing chosen owner.
        self.__owner_logins = None  # list of logins of all owners stored on disk

    @property
    def active_owner(self):
        return self.__active_owner_id

    @active_owner.setter
    def active_owner(self, value: int):
        self.__active_owner_id = value

    @property
    def owners(self):
        return self.__owners

    def create_owner(self, login: str, password: str, **kwargs):
        self.__owners.append(Owner(login=login, password=password, **kwargs))

    def delete_owner_by_login(self, del_login: str):
        del_id = None
        for i, owner in enumerate(self.owners):
            if owner.login == del_login:
                del_id = i
        if del_id:
            del self.owners[del_id]
            log.info(datetime.now().strftime(DiaryApp.cfg.log_time_format) +
                     f"Owner login = {del_login} was deleted")
        else:
            log.error(datetime.now().strftime(DiaryApp.cfg.log_time_format) +
                      f"Owner login = {del_login} was not found.")
            raise ValueError(f"Owner login = {del_login} was not found.")

    def save_data_to_disc(self):
        # check path where to store data from config file
        # make directory if needed
        if not os.path.isdir(DiaryApp.cfg.dir_path):
            os.mkdir(DiaryApp.cfg.dir_path)
        self.set_config_first_use_false()
        owners_logins = [o.login for o in self.owners]
        # Saves every Owner separately
        for o_index, login in enumerate(owners_logins):
            owner_file_path = DiaryApp.cfg.dir_path + login + DiaryApp.cfg.data_extension
            try:
                with open(owner_file_path, mode="wb") as f:
                    pickle.dump(obj=self.owners[o_index], file=f, protocol=pickle.HIGHEST_PROTOCOL)
            except IOError as e:
                log.error(datetime.now().strftime(DiaryApp.cfg.log_time_format) + f"Error writing to {owner_file_path} file. {e}")
                raise RuntimeError(f"Can't open the file {owner_file_path} to save data.")

        try:
            owner_path = DiaryApp.cfg.dir_path + DiaryApp.cfg.owner_login_file_name
        except KeyError:
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
        self.__owner_logins = DiaryApp.load_owners_names_from_disk()
        # load all data about owners
        for o_index, login in enumerate(self.__owner_logins):
            self.owners.append(DiaryApp.load_owner_from_disk(login))

    @classmethod
    def set_config_first_use_false(cls):
        # No exception should occur. This property of cfg was already addressed.
        cls.cfg.first_use = False
        cls.cfg.save()

    @classmethod
    def load_owners_names_from_disk(cls):
        try:
            # tries to find Owner logins file path in config file
            owner_path = DiaryApp.cfg.dir_path + DiaryApp.cfg.owner_login_file_name
        except KeyError:
            log.error(datetime.now().strftime(DiaryApp.cfg.log_time_format) + "Cannot locate 'diary:owner_login_file_name' in config file")
            raise RuntimeError("Config file has been corrupted. 'diary:owner_login_file_name' missing.")

        # try to read the owner logins from file
        try:
            with open(owner_path, mode="rb") as f:
                owners_logins = pickle.load(f)
        except FileNotFoundError:
            log.error(datetime.now().strftime(DiaryApp.cfg.log_time_format) + f"File {owner_path} not found")
            raise RuntimeError(f"File {owner_path} not found. Can't load the data.")
        except IOError as e:
            log.error(datetime.now().strftime(DiaryApp.cfg.log_time_format) + f"Error reading {owner_path} file. {e}")
            raise RuntimeError(f"Can't load the data from {owner_path}.")

        return owners_logins

    @classmethod
    def load_owner_from_disk(cls, login):
        owner_file_path = cls.cfg.dir_path + login + DiaryApp.cfg.data_extension
        try:
            with open(owner_file_path, mode="rb") as f:
                new_owner = pickle.load(file=f)
        except IOError as e:
            log.error(datetime.now().strftime(cls.cfg.log_time_format) + f"Error reading from {owner_file_path} file. {e}")
            raise RuntimeError(f"Can't open the file {owner_file_path} to save data.")
        return new_owner


if __name__ == "__main__":
    app_config = DiaryConfig
    app_config.load()
    main_app = DiaryApp()
    # TODO celé rozhraní
    if main_app.cfg.first_use:
        print("First use was used")
        main_app.create_owner(login="Blad", password="Heslo století")

        main_app.save_data_to_disc()
    else:
        main_app.load_all_data_from_disc()
    print(main_app)

    app_config.save()
