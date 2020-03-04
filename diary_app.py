# @Ondřej Divina & Jan Melichařík

from diary_record import DiaryRecord
from datetime import datetime
import pickle as pickle
import yaml as yaml
import logging as log


class Diary:
    def __init__(self):
        self.owners = []
        with open("config.yml", mode="r") as f:
            self.cfg = yaml.load(f)
        if not self.cfg:
            raise RuntimeError("Cannot find config file.")

        # load path where to store data from config file
        try:
            self.dir_path = self.cfg["diary"]["dir_path"]
        except KeyError as ke:
            log.error(datetime.now().strftime("%d.%m.%Y-%H:%M:%S - ") + "Cannot locate 'diary:dir_path' in config file")
            raise RuntimeError("Config file has been corrupted. diary:dir_path missing.")

        self.active_owner = None

    def save_data_to_disc(self):
        owners_names = [o.name for o in self.owners]
        for o_index, name in enumerate(owners_names):
            owner_file_path = self.dir_path + name + ".Ddata"
            try:
                with open(owner_file_path, mode="wb") as f:
                    pickle.dump(obj=self.owners[o_index], file=f, protocol=pickle.HIGHEST_PROTOCOL)
            except IOError as e:
                log.error(datetime.now().strftime("%d.%m.%Y-%H:%M:%S - ") + f"Error writing to {owner_path} file. {e}")
                raise RuntimeError(f"Can't open the file {owner_file_path} to save data.")

        try:
            owner_path = self.dir_path + self.cfg["diary"]["owner_name_file_name"]
        except KeyError as e:
            log.error(datetime.now().strftime("%d.%m.%Y-%H:%M:%S - ") + "Cannot locate 'diary:owner_name_file_name' in config file")
            raise RuntimeError("Config file has been corrupted. 'diary:owner_name_file_name' missing.")

        try:
            with open(owner_path, mode="wb") as f:
                pickle.dump(obj=owners_names, file=f, protocol=pickle.HIGHEST_PROTOCOL)
        except IOError as e:
            log.error(datetime.now().strftime("%d.%m.%Y-%H:%M:%S - ") + f"Error writing to {owner_path} file. {e}")
            raise RuntimeError(f"Can't open the file {owner_path} to save data.")

    def load_data_from_disc(self):
        try:
            owner_path = self.dir_path + self.cfg["diary"]["owner_name_file_name"]
        except KeyError as e:
            log.error(datetime.now().strftime("%d.%m.%Y-%H:%M:%S - ") + "Cannot locate 'diary:owner_name_file_name' in config file")
            raise RuntimeError("Config file has been corrupted. 'diary:owner_name_file_name' missing.")
        # try to read the owner names from file
        try:
            with open(owner_path) as f:
                owner_names = pickle.load(f)
        except FileNotFoundError as e:
            log.error(datetime.now().strftime("%d.%m.%Y-%H:%M:%S - ") + f"File {owner_path} not found")
            raise RuntimeError(f"File {owner_path} not found. Can't load the data.")
        except IOError as e:
            log.error(datetime.now().strftime("%d.%m.%Y-%H:%M:%S - ") + f"Error reading {owner_path} file. {e}")
            raise RuntimeError(f"Can't load the data from {owner_path}.")

        # load all data about owners
        # TODO do budoucna možná bude potřeba předělat na samostatné načítání po jednom Ownerovi -->
        #  paměťové nároky na načtení všech dat vs jednoho Ownera
        


if __name__ == "__main__":
    Diary()
    print("Welcome to our app")
    records = [
        DiaryRecord(datetime(2020, 2, 23), "Den ve škole", "Ráno jsem šel do školy. Po škole jsem šel domů.\n "
                                                           "Doma to byla sranda."),
        DiaryRecord(datetime(2020, 2, 22), "Pohodová neděle", "Ráno jsem nešel do školy.  Odpoledne byla procházka.\n " 
                                                              "Doma to byla sranda$÷+ěš  .")
        ]
    print(records)


