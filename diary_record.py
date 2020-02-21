from datetime import datetime
import pyperclip as ppc


class DiaryRecord:
    def __init__(self, date, title, text, date_of_creation=None):
        self.date = date
        self.title = title
        self.text = text
        self.date_of_creation = date_of_creation if not date_of_creation else datetime.now()
        self.list_of_alteration_dates = []
        # self.history_of_changes = {}
        # self.list_of_media = []

    def update(self, date: datetime = None, text: str = None, title: str = None, alteration_date: datetime = None):
        """
        Update existing DiaryRecord. Raise TypeError exception if the provided parameters type are not suitable.
        :param date: New date of the record. If None, then no changes in date happen.
        :param text: New text of the record. If None, then no changes in text happen.
        :param title: New title of the record. If None, then no changes in title happen.
        :param alteration_date: Date of the change in record. Current time used if None alternation_date provided
        :return: Nothing.
        """
        # check proper data types
        assert type(text) == str, f"Parameter provided for 'text' is not suitable. Text should be 'string'. Given parameter is: '{type(text)}'"
        assert type(title) == str, f"Parameter provided for 'title' is not suitable. Title should be 'string'. Given parameter is: '{type(title)}'"
        assert type(date) == datetime, f"Parameter provided for 'date' is not suitable. Date should be 'datetime'. Given parameter is: '{type(date)}'"

        self.title = self.title if title is None else title
        self.text = self.text if text is None else text
        self.date = self.date if date is None else date
        self.list_of_alteration_dates.append(datetime.now() if alteration_date is None else alteration_date)

    def __str__(self):
        date_str = self.date.strftime("%d. %m. %Y")
        return f"{date_str} – {self.title}: {self.text}"

    def export_as_text(self):
        ppc.copy(str(self))

    def export(self):
        # todo epxort - možná bude stačit jen ta __str__ reprezentace
        pass
