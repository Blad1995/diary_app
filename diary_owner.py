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
        self.info = OwnerInfo(name, password, photo, email, data_joined)
        self.list_of_diaries = []
        self.bio = bio
        log.info(datetime.now().strftime("%d.%m.%Y-%H:%M:%S - ") + f"New instance of owner was created. {str(self)}")

    def change_password(self, new_password: str, old_password) -> None:
        if self.info.is_password_valid(old_password):
            self.info.password = new_password
        else:
            raise PermissionError("Old password is not valid.")
    
    def create_diary(self, title: str, bio = None):
        """
        Create new Diary and add it to database of Diaries of the Owner
        :param title: Title of the new Diary
        :param bio: Short summary of the new Diary
        :return: True if Diary was created, False otherwise
        """
        new_diary = Diary(title = title, bio = bio, date_of_creation = datetime.now())
        try:
            self.list_of_diaries.append(new_diary)
        except Exception as e:
            log.info(datetime.now().strftime("%d.%m.%Y-%H:%M:%S - ") + f"Failed to create new Diary"
                                                                       f" with parameters: Title: {title}, {bio}, {date_of_creation}\n"
                                                                       f"Exception: {e}")
            return False
        else:
            return True
