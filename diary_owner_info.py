from datetime import datetime


class OwnerInfo:
    def __init__(self, name: str, password, photo=None, email: str = None, date_joined: datetime = None):
        self.name = name
        self.photo = photo
        self.email = email
        self.password = password
        self.date_joined = date_joined if date_joined else datetime.now()
        self.last_active = self.date_joined
