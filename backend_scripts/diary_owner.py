import logging as log
from datetime import datetime

from backend_scripts.diary_book import Diary
from backend_scripts.diary_owner_info import OwnerInfo
from config import DiaryConfig


class Owner:
    """
    Class representing Owner of the diary.
    """
    cfg = DiaryConfig

    def __init__(self, login: str, password: str, **kwargs):
        """
        Create new instance of the class Owner.\n
        :param login: owner login used to log into app
        :param password: new password of the Owner
        :keyword name: name of the Owner
        :keyword email: Owner's email
        :keyword bio: Short personal summary of the Owner
        :keyword photo: photo of the Owner
        :keyword data_joined: Date when the Owner was created in the app.
        """
        self.__info = OwnerInfo(
            name=kwargs.get("name", None),
            login=login,
            password=password,
            photo=kwargs.get("photo", None),
            email=kwargs.get("email", None),
            date_joined=kwargs.get("data_joined", None)
            )
        self.__dict_of_diaries = {}
        self.__bio = kwargs.get("bio", None)
        log.info(datetime.now().strftime(Owner.cfg.log_time_format) +
                 f" - New instance of owner was created. {str(self)}")

    @property
    def login(self):
        return self.__info.login

    @property
    def name(self):
        return self.info.name

    @property
    def info(self):
        return self.__info

    @info.setter
    def info(self, **kwargs):
        # TODO can't set probably
        for key, value in kwargs.items():
            try:
                setattr(self.__info, key, value)
            except AttributeError as e:
                log.warning(datetime.now().strftime(Owner.cfg.log_time_format) +
                            f" - Invalid argument provided for info.setter in Owner - "
                            f"{e}")

    @property
    def bio(self):
        return self.__bio

    @bio.setter
    def bio(self, new_bio):
        self.__bio = new_bio

    @property
    def dict_of_diaries(self):
        return self.__dict_of_diaries

    def change_password(self, new_password: str, old_password) -> None:
        if self.info.is_password_valid(old_password):
            self.info.password = new_password
        else:
            raise PermissionError("Old password is not valid.")

    def is_password_valid(self, pswd_to_check: str):
        return self.info.is_password_valid(pswd_to_check)

    def create_diary(self, title: str, bio = None):
        """
        Create new Diary and add it to database of Diaries of the Owner\n
        :param title: Title of the new Diary
        :param bio: Short summary of the new Diary
        :return: True if Diary was created, False otherwise
        """
        if title in self.dict_of_diaries.keys():
            raise ValueError(f"Diary with such title already exists. Title:{title}")

        date_of_creation = datetime.now()
        new_diary = Diary(title=title, bio=bio, date_of_creation=date_of_creation)
        try:
            # add new Diary to the dictionary
            self.dict_of_diaries[title] = new_diary
        except Exception as e:
            log.info(datetime.now().strftime(Owner.cfg.log_time_format) + f" - Failed to create new Diary"
                                                                          f" with parameters: Title: {title}, {bio}, {date_of_creation}\n"
                                                                          f"Exception: {e}")
            raise e

    def delete_diary(self, title) -> bool:
        """
        Deletes diary stored in the dict_of_diaries\n
        :param title: Title of the Diary. Unique identification.
        :return: True if Diary was successfully deleted. False if there is no diary with such title. Propagate exception if unexpected error occurs
        """
        try:
            del self.dict_of_diaries[title]
        except KeyError as e:
            log.warning(datetime.now().strftime(Owner.cfg.log_time_format) + f" - Failed to delete Diary"
                                                                             f" with parameters: Title: {title}\n"
                                                                             f"Exception: {e}")
            return False
        except Exception as e:
            log.warning(datetime.now().strftime(Owner.cfg.log_time_format) + f" - Failed to delete Diary"
                                                                             f" with parameters: Title: {title}. Exception: "
                                                                             f"{e}")
            raise e
        else:
            log.info(datetime.now().strftime(Owner.cfg.log_time_format) + f" - Deleted Diary"
                                                                          f" with title: {title}")
            return True
