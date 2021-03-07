import logging as log
from datetime import datetime

from config import DiaryConfig


class OwnerInfo:
    """
    Class representing personal info of the Owner.
    """
    cfg = DiaryConfig

    def __init__(self, login: str, password, name: str = None, photo = None, email: str = None, date_joined: datetime = None):
        """
        Create new instance of OwnerInfo class with following parameters.\n
        :param name: Name of the owner
        :param password: New password in the form of the string
        :param photo: Photo of the owner
        :param email: Email address of the owner
        :param date_joined: Date on which the owner was added to application (created in app)
        """
        assert type(name) in [str, type(None)]
        assert type(login) == str
        assert type(email) in [str, type(None)]

        self._name = name
        self._login = login
        self._photo = photo
        self._email = email
        # for develompent purposes string --> TODO more secure solution
        # so far it's marked as private
        self._password = password
        # should be constant after creation
        self._date_joined = date_joined if date_joined else datetime.now()
        self._last_active = self._date_joined
        log.info(datetime.now().strftime(OwnerInfo.cfg.log_time_format) +
                 f" - New instance of owner info was created. {str(self)}")

    def __eq__(self, other):
        return self._login == other.login

    def __hash__(self):
        return self.login.__hash__()

    # Name setters & getters
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        log.info(datetime.now().strftime(OwnerInfo.cfg.log_time_format) +
                 f" - Name of the owner was updated from '{self.name}' to '{name}'")
        self._name = name

    @property
    def login(self):
        return self._login

    @login.setter
    def login(self, value):
        log.info(datetime.now().strftime(OwnerInfo.cfg.log_time_format) +
                 f" - Login of the owner was updated from '{self.login}' to '{value}'")
        self._login = value

    # Photo setters & getters
    @property
    def photo(self):
        return self._photo

    @photo.setter
    def photo(self, photo):
        log.info(datetime.now().strftime(OwnerInfo.cfg.log_time_format) +
                 f" - Photo of the owner was updated.'")
        self._photo = photo

    # email setters & getters
    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        log.info(datetime.now().strftime(OwnerInfo.cfg.log_time_format) +
                 f" - Email of the owner {self.name} was updated from '{self.email}' to '{email}'")
        self._email = email

    # password setters & getters
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        log.info(datetime.now().strftime(OwnerInfo.cfg.log_time_format) +
                 f" - Password of the owner {self.name} was updated.'")
        self._password = password

    @property
    def last_active(self):
        return self._last_active

    @last_active.setter
    def last_active(self, last_active):
        log.debug(datetime.now().strftime(OwnerInfo.cfg.log_time_format) +
                  f" - Last active variable of the owner {self.name} was updated from '{self.last_active}' to '{last_active}'")
        self._last_active = last_active

    @property
    def date_joined(self):
        return self._date_joined

    def __str__(self):
        return f"Login:{self.login}, name: {self.name}, email: {self.email}, created: {self.date_joined}"

    def is_password_valid(self, password: str) -> bool:
        """
        Determines if password is valid.\n
        :param password: string of the password to be tested
        :return: Bool value
        """
        # TODO more secured solution
        return password == self.password
