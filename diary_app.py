# @Ondřej Divina & Jan Melichařík

import logging as log
import os as os
import pickle as pickle
from datetime import datetime

# my modules
from backend_scripts.diary_owner import Owner
from backend_scripts.diary_owner_info import OwnerInfo
from config import DiaryConfig


class DiaryControl:
    """
    Controls whole app Diary. Contains methods for storing and loading data from files and stores all owners and other data.
    """
    cfg = DiaryConfig  # :class variable for storing loaded config file.

    def __init__(self, config_path: str = None):
        """
        Initialize empty class.
        """
        self.__owners_dict: dict or None = {}  # Contains all owners of the diaries.
        if config_path is None:
            self.cfg.load()
        else:
            self.cfg.load(config_path)

    @property
    def owners(self):
        """
        Get the list of owners (Owner class from owner.py)
        :return: list[Owner]
        """
        return list(self.__owners_dict.values())

    @property
    def owners_info(self):
        """
        Get the list of owners info (OwnerInfo class from owner_info.py)
        :return: list[OwnerInfo]
        """
        return list(self.__owners_dict.keys())

    def create_owner(self, login: str, password: str, **kwargs):
        """
        Creates Owner and adds it into class owners list.\n

        :param login: Login of the new owner
        :param password: Password of the new owner
        :param kwargs: see below
        :return: new Owner that was created

        :keyword name: name of the Owner
        :keyword email: Owner's email
        :keyword bio: Short personal summary of the Owner
        :keyword photo: photo of the Owner
        :keyword data_joined: Date when the Owner was created in the app.

        :raise ValueError: if login is not unique
        """
        new_owner = Owner(login=login, password=password, **kwargs)
        # check uniqueness of login
        if self.get_owner_by_login(login) is not None:
            log.error(datetime.now().strftime(DiaryControl.cfg.log_time_format) +
                      f"Owner login = {login} already exists.")
            raise ValueError(f"Owner login = {login} already exists.")
        else:
            # add owner to dict and return it
            self.__owners_dict[new_owner.info] = new_owner
            return new_owner

    def delete_owner_by_login(self, del_login: str):
        """
        Deletes owner from DiaryControl. Also deletes all the data stored on the disc.\n
        :param del_login: Login of the owner that should be deleted

        :raise ValueError: if the login is invalid (not found).
        """
        del_owner_info = None
        for i, owner_info in enumerate(self.owners_info):
            if owner_info.login == del_login:
                # finds the right owner in list and store the location
                del_owner_info = owner_info

        if del_id is not None:
            # delete data from disc
            self.erase_data_files(del_id)
            # delete key_value pair from dict (even if owner not loaded)
            del self.__owners_dict[del_owner_info]
            # self.update_owner_info_list()
            log.info(datetime.now().strftime(DiaryControl.cfg.log_time_format) +
                     f" - Owner login = {del_login} was deleted")
        else:
            log.error(datetime.now().strftime(DiaryControl.cfg.log_time_format) +
                      f" - Owner login = {del_login} was not found.")
            raise ValueError(f"Owner login = {del_login} was not found.")

    def save_owners_to_disc(self):
        """
        Save all owners loaded in DiaryControl instance to the disc.\n
        Uses config values to store define file location of the result data files.\n
        :raise RuntimeError: if the file path is not valid and can't save the data
        """
        owners_logins = [o.login for o in self.owners_info]
        # Saves every Owner separately
        for login in owners_logins:
            owner_file_path = os.path.join(DiaryControl.cfg.dir_path, login) + DiaryControl.cfg.data_extension
            try:
                with open(owner_file_path, mode="wb") as f:
                    # dumps pickled Owner data to disc
                    pickle.dump(obj=self.get_owner_by_login(login),
                                file=f,
                                protocol=pickle.HIGHEST_PROTOCOL)
            except IOError as e:
                log.error(datetime.now().strftime(DiaryControl.cfg.log_time_format) +
                          f" - Error writing to {owner_file_path} file. {e}")
                raise RuntimeError(f"Can't open the file {owner_file_path} to save data.")

    def save_owners_info_to_disc(self):
        """
        Saves the data of the OwnerInfo list stored in DiaryControl instance.\n
        :raise RuntimeError: if config doesn't have destination path values.
        :raise RuntimeError: if can't open destination file
        """
        try:
            owner_path = os.path.join(DiaryControl.cfg.dir_path, DiaryControl.cfg.owner_credentials_file_name)
        except KeyError:
            log.error(datetime.now().strftime(DiaryControl.cfg.log_time_format) +
                      " - Cannot locate 'diary:owner_credentials_file_name' in config file")
            raise RuntimeError("Config file has been corrupted. 'diary:owner_credentials_file_name' missing.")

        self.update_owner_info_list()
        try:
            # Saves owners login to file
            with open(owner_path, mode="wb") as f:
                pickle.dump(obj=list(self.__owners_dict.keys()), file=f, protocol=pickle.HIGHEST_PROTOCOL)
        except IOError as e:
            log.error(datetime.now().strftime(DiaryControl.cfg.log_time_format) +
                      f" - Error writing to {owner_path} file. {e}")
            raise RuntimeError(f"Can't open the file {owner_path} to save data.")

    def save_data_to_disc(self):
        """
        Saves all data stored in the instance of DiaryControl class. Including owners and owners_info.\n
        Saves the config with the first_use=false
        """
        # Save owners info and owners data
        self.save_owners_to_disc()
        self.save_owners_info_to_disc()

        # check path where to store data from config file
        # make directory if needed
        if not os.path.isdir(DiaryControl.cfg.dir_path):
            os.mkdir(DiaryControl.cfg.dir_path)
        # set config value first use to false and saves the config
        self.set_config_first_use_false()

    def load_all_data_from_disc(self):
        """
        Loads all data from disc to the instance of DiaryControl class.\n
        First loads all owners_info and then loads corresponding data of the owners\n
        :raise RuntimeError: if can't find data of the owners stored in owners_info
        """
        # setup temporary dict with all loaded keys (they will be replaced after load of owners)
        self.__owners_dict = dict.fromkeys(DiaryControl.load_owners_info_from_disc(), None)
        # load all data about owners
        for o_info in self.__owners_dict.keys():
            try:
                new_owner = DiaryControl.load_owner_from_disc(o_info.login)
            except RuntimeError as e:
                log.error(datetime.now().strftime(DiaryControl.cfg.log_time_format) +
                          f" - Error loading {o_info.login} owner from disc. Data structure corrupted.{e}")
                raise RuntimeError(f"Unable to load {o_info.login} owner.")
            # replace old entry by new loaded entry
            del self.__owners_dict[o_info]
            self.__owners_dict[new_owner.info] = new_owner

    @classmethod
    def set_config_first_use_false(cls):
        """
        Changes *first_use* value in config to false and saves config.
        """
        # No exception should occur. This property of cfg was already addressed.
        cls.cfg.first_use = False
        cls.cfg.save()

    def get_owner_by_login(self, login: str, default = None):
        """
        Get owner from the dictionary stored in DiaryControl by login.\n
        :param login: login of the owner to be returned
        :param default: default value that should be returned if no owner found.
        :return: reference to the found Owner
        """
        return self.__owners_dict.get(OwnerInfo(login=login, password=None), default)

    @classmethod
    def load_owners_info_from_disc(cls):
        """
        Loads all owners_info from disc. Loading path is defined by config file.\n
        :return: loaded list of owner_info --> list[OwnerInfo]
        :raise RuntimeError: if data cannot be loaded from disc for various reasons
        """
        try:
            # tries to find Owner logins file path in config file
            owner_path = DiaryControl.cfg.dir_path + DiaryControl.cfg.owner_credentials_file_name
        except KeyError:
            log.error(datetime.now().strftime(DiaryControl.cfg.log_time_format) +
                      " - Cannot locate 'diary:owner_credentials_file_name' in config file")
            raise RuntimeError("Config file has been corrupted. 'diary:owner_credentials_file_name' missing.")

        # try to read the owner info from file
        try:
            with open(owner_path, mode="rb") as f:
                owners_info = pickle.load(f)
        except FileNotFoundError:
            log.error(datetime.now().strftime(DiaryControl.cfg.log_time_format) +
                      f" - File {owner_path} not found")
            raise RuntimeError(f"File {owner_path} not found. Can't load the data.")
        except IOError as e:
            log.error(datetime.now().strftime(DiaryControl.cfg.log_time_format) +
                      f" - Error reading {owner_path} file. {e}")
            raise RuntimeError(f"Can't load the data from {owner_path}.")

        return owners_info

    @classmethod
    def load_owner_from_disc(cls, login: str) -> Owner or None:
        """
        Loads one owner from disc using his login.\n
        Loading path is defined in config file (dir_path, data_extension).\n
        :param login: Login of the owner to be loaded
        :return: reference to the loaded Owner
        :raise RuntimeError: if cannot load the data from the disc
        """
        owner_file_path = cls.cfg.dir_path + login + cls.cfg.data_extension
        try:
            with open(owner_file_path, mode="rb") as f:
                new_owner = pickle.load(file=f)
        except FileNotFoundError:
            log.error(datetime.now().strftime(DiaryControl.cfg.log_time_format) +
                      f" - File {owner_file_path} not found")
            raise RuntimeError(f"File {owner_file_path} not found. Can't load the data.")
        except IOError as e:
            log.error(datetime.now().strftime(cls.cfg.log_time_format) +
                      f" - Error reading from {owner_file_path} file. {e}")
            raise RuntimeError(f"Can't open the file {owner_file_path} to load data.")
        return new_owner

    def update_owner_info_list(self):
        """
        NotImplementedError\n
        Update all the information in the list of owners_info"""
        # TODO maybe wont be needed
        raise NotImplementedError("update_owner_info_list NOT IMPLEMENTED")

    def erase_data_files(self, del_id):
        login = self.owners_info[del_id].login
        owner_file_path = self.cfg.dir_path + login + self.cfg.data_extension
        try:
            os.remove(owner_file_path)
        except FileNotFoundError as e:
            log.error(datetime.now().strftime(self.cfg.log_time_format) +
                      f" - Error deleting {owner_file_path} file. {e}")


if __name__ == "__main__":
    app_config = DiaryConfig
    app_config.load()
    main_app = DiaryControl()

    # TODO celé rozhraní
    if main_app.cfg.first_use:
        print("First use was used")
        main_app.create_owner(login="Blad", password="Heslo století")

        main_app.save_data_to_disc()
    else:
        main_app.load_all_data_from_disc()
    print(main_app)

    app_config.save()
