from diary_owner_info import OwnerInfo
import logging as log
from datetime import datetime


class Owner:
    """
    Class representing Owner of the diary.
    """
    def __init__(self, name: str, password: str, email = None, bio: str = None, photo = None, data_joined = datetime.now()):
        """
        Create new instance of the class Owner.
        :param name: name of the Owner
        :param password: new password of the Owner
        :param email: Owner's email
        :param bio: Short personal summary of the Owner
        :param photo: photo of the Owner
        :param data_joined: Date when the Owner was created in the app.
        """
        info = OwnerInfo(name, password, photo, email, data_joined)
        list_of_diaries = []
        bio = bio
        log.info(datetime.now().strftime("%d.%m.%Y-%H:%M:%S - ") + f"New instance of owner was created. {str(self)}")

