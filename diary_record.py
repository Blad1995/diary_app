import logging as log
import re as re
from datetime import datetime

import pyperclip as ppc

from config import DiaryConfig


class DiaryRecord:
    __IMPORT_PATTERN = r"^(\d{1,2}\. \d{1,2}\. \d{4}) – (.+): (.+)$"
    cfg = DiaryConfig

    def __init__(self, date: datetime, title: str, text: str, date_of_creation = None):
        self.__date = date
        self.__title = title
        self.__text = text
        self.__date_of_creation = date_of_creation if date_of_creation else datetime.now()
        self.__list_of_alteration_dates = []
        # self.__history_of_changes = {}
        # self.__list_of_media = []

        log.info(datetime.now().strftime(DiaryRecord.cfg.log_time_format) + f" - Diary Record was created: {str(self)}")

    # ↓Setters and getters ----------------------------------------------------------
    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, new_date: datetime):
        self.__date = new_date

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, new_title: str):
        self.__title = new_title

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, new_text: str):
        self.__text = new_text

    @property
    def date_of_creation(self):
        return self.__date_of_creation

    @date_of_creation.setter
    def date_of_creation(self, new_date: datetime):
        self.__date_of_creation = new_date

    @property
    def list_of_alteration_dates(self):
        return self.__list_of_alteration_dates

    @list_of_alteration_dates.setter
    def list_of_alteration_dates(self, new_date: datetime):
        self.__list_of_alteration_dates.append(new_date)
    # ↑ Getters and setters _______________________________________

    def update(self, date: datetime = None, text: str = None, title: str = None, alteration_date: datetime = None) -> None:
        """
        Update existing DiaryRecord. Raise TypeError exception if the provided parameters type are not suitable.
        :param date: New date of the record. If None, then no changes in date happen.
        :param text: New text of the record. If None, then no changes in text happen.
        :param title: New title of the record. If None, then no changes in title happen.
        :param alteration_date: Date of the change in record. Current time used if None alternation_date provided
        :return: Nothing.
        """
        # check proper data types
        assert type(text) == str, f"Parameter provided for 'text' is not suitable." \
                                  f" Text should be 'string'. Given parameter is: '{type(text)}'"
        assert type(title) == str, f"Parameter provided for 'title' is not suitable." \
                                   f" Title should be 'string'. Given parameter is: '{type(title)}'"
        assert type(date) == datetime, f"Parameter provided for 'date' is not suitable." \
                                       f" Date should be 'datetime'. Given parameter is: '{type(date)}'"

        self.__title = self.__title if title is None else title
        self.__text = self.__text if text is None else text
        self.__date = self.__date if date is None else date
        self.__list_of_alteration_dates.append(datetime.now() if alteration_date is None else alteration_date)

        log.info(datetime.now().strftime(DiaryRecord.cfg.log_time_format) + f" - Diary Record was updated: {str(self)}")

    def __str__(self):
        date_str = self.__date.strftime("%d. %m. %Y")
        return f"{date_str} – {self.__title}: {self.__text}"

    def __repr__(self):
        repr_string = f"DiaryRecord instance\nDate: {self.__date}\nTitle: {self.__title}\n" \
                      f"Text: {self.__text}\nDate of creation: {self.__date_of_creation}\n"
        repr_string += "Dates of alternation:\n"
        for a_date in self.__list_of_alteration_dates:
            repr_string += str(a_date) + "\n"
        return repr_string

    def export_to_clipboard(self) -> None:
        """
        Function for copying DiaryRecord to clipboard.
        """
        ppc.copy(str(self))

    def export(self):
        # todo export - možná bude  jen ta __str__ reprezentace
        pass

    @classmethod
    def import_from_text(cls, text: str) -> "DiaryRecord":
        """
        :param cls: DiaryRecord class
        :param text: Text from which the info about DiaryRecord would be extracted.
        :return: new DiaryRecord instance
        """
        if re.search(DiaryRecord.__IMPORT_PATTERN,   text):
            parsed_text = re.match(DiaryRecord.__IMPORT_PATTERN, text)
            # Assign each parsed group to corresponding variable
            date, title, text = parsed_text.groups()

            log.info(datetime.now().strftime(DiaryRecord.cfg.log_time_format) + f" - Imported text was parsed as: {parsed_text.groups()}")
            return DiaryRecord(date=date, title=title, text=text)
        else:
            raise ValueError(f"Format of the text to import is invalid. Expected format:\n{DiaryRecord.__IMPORT_PATTERN}")
