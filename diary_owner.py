import logging as log
from datetime import datetime
from diary_owner_info import OwnerInfo
from diary_book import Diary


class Owner:
    """
    Class representing Owner of the diary.
    """
    def __init__(self, name: str, password: str, email = None, bio: str = None, photo = None, data_joined = None):
        """
        Create new instance of the class Owner.
        :param name: name of the Owner
        :param password: new password of the Owner
        :param email: Owner's email
        :param bio: Short personal summary of the Owner
        :param photo: photo of the Owner
        :param data_joined: Date when the Owner was created in the app.
        """
        self.__info = OwnerInfo(name, password, photo, email, data_joined)
        self.__list_of_diaries = []
        self.__bio = bio
        log.info(datetime.now().strftime("%d.%m.%Y-%H:%M:%S - ") + f"New instance of owner was created. {str(self)}")

    @property
    def info(self):
        return self.__info

    @info.setter
    def info(self, **kwargs):
        for key, value in kwargs.items():
            try:
                setattr(self.__info, key, value)
            except AttributeError as e:
                log.warning(datetime.now().strftime("%d.%m.%Y-%H:%M:%S - ") + f"Invalid argument provided for info.setter in Owner - "
                                                                              f"{e}")

    @property
    def bio(self):
        return self.__bio

    @bio.setter
    def bio(self, new_bio):
        self.__bio = new_bio

    def change_password(self, new_password: str, old_password) -> None:
        if self.__info.is_password_valid(old_password):
            self.__info.password = new_password
        else:
            raise PermissionError("Old password is not valid.")
    
    def create_diary(self, title: str, bio = None):
        """
        Create new Diary and add it to database of Diaries of the Owner
        :param title: Title of the new Diary
        :param bio: Short summary of the new Diary
        :return: True if Diary was created, False otherwise
        """
        new_diary = Diary(title=title, bio=bio, date_of_creation=datetime.now())
        try:
            self.__list_of_diaries.append(new_diary)
        except Exception as e:
            log.info(datetime.now().strftime("%d.%m.%Y-%H:%M:%S - ") + f"Failed to create new Diary"
                                                                       f" with parameters: Title: {title}, {bio}, {date_of_creation}\n"
                                                                       f"Exception: {e}")
            return False
        else:
            return True
