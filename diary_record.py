from datetime import datetime


class DiaryRecord:
    def __init__(self, date, text, date_of_creation=None):
        self.date = date
        self.text = text
        self.date_of_creation = date_of_creation if not date_of_creation else datetime.now()
        self.list_of_alteration_dates = []
        # self.history_of_changes = {}
        self.list_of_media = []
