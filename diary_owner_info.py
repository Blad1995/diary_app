from datetime import datetime
import logging as log


class OwnerInfo:
    """
    Class representing personal info of the Owner.
    """
    def __init__(self, name: str, password, photo=None, email: str = None, date_joined: datetime = None):
        """
        Create new instance of OwnerInfo class with following parameters.
        :param name: Name of the owner
        :param password: New password in the form of the string
        :param photo: Photo of the owner
        :param email: Email address of the owner
        :param date_joined: Date on which the owner was added to application (created in app)
        """
        self.__name = name
        self.__photo = photo
        self.__email = email
        # for develompent purposes string --> TODO more secure solution
        # so far it's marked as private
        self.__password = password
        # should be constant after creation
        self.__date_joined = date_joined if date_joined else datetime.now()
        self.__last_active = self.__date_joined
        log.info(datetime.now().strftime("%d.%m.%Y-%H:%M:%S - ") + f"New instance of owner info was created. {str(self)}")

    # Name setters & getters
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        log.info(datetime.now().strftime("%d.%m.%Y-%H:%M:%S - ") + f"Name of the owner was updated from '{self.name}' to '{name}'")
        self.__name = name

    # Photo setters & getters
    @property
    def photo(self):
        return self.__photo

    @photo.setter
    def photo(self, photo):
        log.info(datetime.now().strftime("%d.%m.%Y-%H:%M:%S - ") + f"Photo of the owner was updated.'")
        self.__photo = photo

    # email setters & getters
    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email):
        log.info(datetime.now().strftime("%d.%m.%Y-%H:%M:%S - ") + f"Email of the owner {self.name} was updated from '{self.email}' to '{email}'")
        self.__email = email

    # password setters & getters
    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        log.info(datetime.now().strftime("%d.%m.%Y-%H:%M:%S - ") + f"Password of the owner {self.name} was updated.'")
        self.__password = password

    @property
    def last_active(self):
        return self.__last_active

    @last_active.setter
    def last_active(self, last_active):
        log.debug(datetime.now().strftime("%d.%m.%Y-%H:%M:%S - ") + f"Last active variable of the owner {self.name} was updated from '{self.last_active}' to '{last_active}'")
        self.__last_active = last_active

    @property
    def date_joined(self):
        return self.__date_joined

    def __str__(self):
        return f"{self.name}, email: {self.email}, created: {self.date_joined}"

    def is_password_valid(self, password: str) -> bool:
        """
        Determines if password is valid.
        :param password: string of the password to be tested
        :return: Bool value
        """
        # TODO more secured solution
        return password == self.password