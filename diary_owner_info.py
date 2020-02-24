from datetime import datetime


class OwnerInfo:
    def __init__(self, name: str, password, photo=None, email: str = None, date_joined: datetime = None):
        self.name = name
        self.photo = photo
        self.email = email
        # for develompent purposes string --> TODO more secure solution
        # so far it's marked as private
        self.__password = password
        # should be constant after creation
        self.date_joined = date_joined if date_joined else datetime.now()
        self.last_active = self.date_joined

    # Name setters & getters
    @property
    def name(self):
        return self.name

    @name.setter
    def name(self, name):
        self.name = name

    # Photo setters & getters
    @property
    def photo(self):
        return self.photo

    @photo.setter
    def photo(self, photo):
        self.photo = photo

    # email setters & getters
    @property
    def email(self):
        return self.email

    @email.setter
    def email(self, email):
        self.email = email

    # password setters & getters
    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        self.__password = password

    @property
    def last_active(self):
        return self.last_active

    @last_active.setter
    def last_active(self, last_active):
        self.last_active = last_active
