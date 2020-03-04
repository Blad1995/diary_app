# @Ondřej Divina & Jan Melichařík

from diary_record import DiaryRecord
from datetime import datetime
import pickle as pickle
import yaml as yaml
import logging as log
import os as os
# my modules
from diary_owner import Owner


class Diary:
    def __init__(self):
        self.owners = []
        with open("config.yml", mode="r") as f:
            self.cfg = yaml.safe_load(f)
        if not self.cfg:
            raise RuntimeError("Cannot find config file.")

        # load path where to store data from config file
        try:
            self.dir_path = self.cfg["diary"]["dir_path"]
        except KeyError as ke:
            log.error(datetime.now().strftime("%d.%m.%Y-%H:%M:%S - ") + "Cannot locate 'diary:dir_path' in config file")
            raise RuntimeError("Config file has been corrupted. diary:dir_path missing.")
        else:
            if not os.path.isdir(self.dir_path):
                os.mkdir(self.dir_path)

        self.active_owner = None

    def save_data_to_disc(self):
        self.set_config_first_use_false()
        owners_names = [o.name for o in self.owners]
        # Saves every Owner separately
        for o_index, name in enumerate(owners_names):
            owner_file_path = self.dir_path + name + ".Ddata"
            try:
                with open(owner_file_path, mode="wb") as f:
                    pickle.dump(obj=self.owners[o_index], file=f, protocol=pickle.HIGHEST_PROTOCOL)
            except IOError as e:
                log.error(datetime.now().strftime("%d.%m.%Y-%H:%M:%S - ") + f"Error writing to {owner_file_path} file. {e}")
                raise RuntimeError(f"Can't open the file {owner_file_path} to save data.")

        try:
            owner_path = self.dir_path + self.cfg["diary"]["owner_name_file_name"]
        except KeyError as e:
            log.error(datetime.now().strftime("%d.%m.%Y-%H:%M:%S - ") + "Cannot locate 'diary:owner_name_file_name' in config file")
            raise RuntimeError("Config file has been corrupted. 'diary:owner_name_file_name' missing.")

        try:
            # Saves owners name to file
            with open(owner_path, mode="wb") as f:
                pickle.dump(obj=owners_names, file=f, protocol=pickle.HIGHEST_PROTOCOL)
        except IOError as e:
            log.error(datetime.now().strftime("%d.%m.%Y-%H:%M:%S - ") + f"Error writing to {owner_path} file. {e}")
            raise RuntimeError(f"Can't open the file {owner_path} to save data.")

    def load_data_from_disc(self):
        try:
            # tries to find Owner names file path in config file
            owner_path = self.dir_path + self.cfg["diary"]["owner_name_file_name"]
        except KeyError as e:
            log.error(datetime.now().strftime("%d.%m.%Y-%H:%M:%S - ") + "Cannot locate 'diary:owner_name_file_name' in config file")
            raise RuntimeError("Config file has been corrupted. 'diary:owner_name_file_name' missing.")

        # try to read the owner names from file
        try:
            with open(owner_path, mode="rb") as f:
                owners_names = pickle.load(f)
        except FileNotFoundError as e:
            log.error(datetime.now().strftime("%d.%m.%Y-%H:%M:%S - ") + f"File {owner_path} not found")
            raise RuntimeError(f"File {owner_path} not found. Can't load the data.")
        except IOError as e:
            log.error(datetime.now().strftime("%d.%m.%Y-%H:%M:%S - ") + f"Error reading {owner_path} file. {e}")
            raise RuntimeError(f"Can't load the data from {owner_path}.")

        # load all data about owners
        # FIXME do budoucna možná bude potřeba předělat na samostatné načítání po jednom Ownerovi -->
        #  paměťové nároky na načtení všech dat vs jednoho Ownera
        for o_index, name in enumerate(owners_names):
            owner_file_path = self.dir_path + name + ".Ddata"
            try:
                with open(owner_file_path, mode="rb") as f:
                    new_owner = pickle.load(file=f)
                    self.owners.append(new_owner)
            except IOError as e:
                log.error(datetime.now().strftime("%d.%m.%Y-%H:%M:%S - ") + f"Error writing to {owner_path} file. {e}")
                raise RuntimeError(f"Can't open the file {owner_file_path} to save data.")

    def set_config_first_use_false(self):
        # No exception should occur. This property of cfg was already addressed.
        self.cfg["general"]["first_use"] = False
        try:
            with open("config.yml", "wb") as f:
                yaml.dump(data=self.cfg, stream=f)
        except IOError as e:
            log.error(datetime.now().strftime("%d.%m.%Y-%H:%M:%S - ") + f"Error writing to config.yml file. {e}")


if __name__ == "__main__":
    main_app = Diary()
    if main_app.cfg["general"]["first_use"]:
        print("First use was used")
        main_app.owners.append(Owner(name="Ondra Divina", password="Heslo století"))

        main_app.save_data_to_disc()
    else:
        main_app.load_data_from_disc()
    print(main_app)



