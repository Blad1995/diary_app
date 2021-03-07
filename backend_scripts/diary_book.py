import logging as log
import os as os
from datetime import datetime

from backend_scripts.diary_record import DiaryRecord
from backend_scripts.two_way_dict import TwoWayDict
# my modules
from config import DiaryConfig


class Diary:
    """
    Class representing whole Diary book.\n
    :var cfg: class variable for storing loaded config file.
    """
    cfg = DiaryConfig

    def __init__(self, title: str, date_of_creation: datetime = None, dict_of_records: dict = None, bio: str = None):
        """
        Initialize Diary class.\n
        :param title: Title of the whole Diary book.
        :param date_of_creation: Date when the Diary was created.
        :param dict_of_records: dictionary containing all existing DiaryRecords.
        :param bio: Short summary about the Diary book.
        """
        self._title = title
        self._date_of_creation = date_of_creation if date_of_creation else datetime.today()
        self._dict_of_records = dict_of_records if dict_of_records else {}
        self._bio = bio
        self._dict_of_removed_records = {}
        self._id_date_relation_dict = TwoWayDict()
        self._last_id: int = max(dict_of_records.keys()) if dict_of_records else None
        log.info(datetime.now().strftime(f"{Diary.cfg.log_time_format} - ") +
                 f"Diary was created {str(self)}")

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value: str):
        self._title = value

    @property
    def bio(self):
        return self._bio

    @bio.setter
    def bio(self, value: str):
        self._bio = value

    @property
    def date_of_creation(self):
        return self._date_of_creation

    @property
    def dict_of_records(self):
        return self._dict_of_records

    @property
    def dict_of_removed_records(self):
        return self._dict_of_removed_records

    def __str__(self):
        date_str = self.date_of_creation.strftime("%d. %m. %Y")
        string = f"Title: {self.title}, created on {date_str}"
        return string

    def delete_record(self, record_id: int):
        if record_id in self.dict_of_records:
            self.dict_of_removed_records[record_id] = self.dict_of_records.pop(record_id)
            del self._id_date_relation_dict[record_id]
        else:
            log.warning(datetime.now().strftime(f"{Diary.cfg.log_time_format} - ") +
                        f"No such record with id = {record_id} in diary {str(self)}")
            raise ValueError(f"Diary record number {record_id} doesn't exist")

    def export_to_txt(self, destination: str):
        """
        Export whole Diary with records to txt\n
        :param destination: Folder path where the result should be written.
        """
        if not os.path.isdir(destination):
            raise FileNotFoundError(f"{destination} is not a valid directory.")
        file_path = destination.rstrip("/") + "/" + f'{self.title.lower()}_{self.date_of_creation.strftime(self.cfg.date_format)}.txt'
        try:
            with open(file_path, 'w') as f:
                payload = str(
                    {
                        'title': self.title,
                        'date_of_creation': self.date_of_creation.strftime(self.cfg.date_format),
                        'bio': self.bio,
                        'records': "\n"
                        })
                for record in self.dict_of_records.values():
                    payload += "___________________\n"
                    payload += f"{record}"
                    payload += "\n"
                f.write(payload)
        except IOError as e:
            log.error(datetime.now().strftime(f"{Diary.cfg.log_time_format} - ") +
                      f"Error writing to {file_path}. {e}")
            raise e

    def create_record(self, date_of_record: datetime, title: str, text: str, date_of_creation: datetime = None):
        """
        Creates new record and adds it to the dict_of_records. Raise exception if only something unexpected happens.\n
        Accepts parameters of the strict type.\n
        :type date_of_creation: datetime
        :type text: str
        :type title: str
        :type date_of_record: datetime
        :param date_of_record: Date of the record. The day which the record is about.
        :param title: Title of the diary record.
        :param text: Text of the record. Can be multi-line
        :param date_of_creation: Date of creation of the record. In default takes system datetime
        """
        assert type(date_of_record) == datetime
        assert type(title) == str
        assert type(text) == str

        if self._last_id is None:
            self._last_id = 0
        else:
            self._last_id += 1

        if self.dict_of_records.get(self._last_id, None):
            # If record with this id already exist (it shouldn't) reset the counter
            self._last_id = max(self.dict_of_records.keys())
            log.warning(datetime.now().strftime(f"{Diary.cfg.log_time_format} - ") +
                        f"id: {self._last_id} is already taken! last_id counter was reset")

        try:
            self.dict_of_records[self._last_id] = DiaryRecord(id=self._last_id,
                                                              date=date_of_record,
                                                              title=title,
                                                              text=text,
                                                              date_of_creation=date_of_creation)
            self._id_date_relation_dict[self._last_id] = date_of_record
        except Exception as e:
            log.error(datetime.now().strftime(f"{Diary.cfg.log_time_format} - ") +
                      f"Unexpected error when creating the record in Diary. {e}")
            log.debug(f"Parameters of Diary.create_record: Title:{title}, date_of_record: {date_of_record}, text={text}")
            raise e

    def update_record(self, record_id: int, date_of_record: datetime = None, text: str = None, title: str = None):
        """
        Updates information about the record identified by given record_id.\n
        :param record_id: id of the record to be updated
        :param date_of_record: new date of the record
        :param text: new text of the record
        :param title: new title of the record
        :raise ValueError if no such record found.
        """
        record_to_update: DiaryRecord = self.dict_of_records.get(record_id, None)
        if record_to_update:
            record_to_update.update(date=date_of_record, text=text, title=title)
        else:
            log.warning(datetime.now().strftime(f"{Diary.cfg.log_time_format} - ") +
                        f"No such diary record with id = {record_id}")
            raise ValueError(f"Diary record number {record_id} doesn't exist")

    def get_record_by_id(self, record_id: int, default = None):
        return self.dict_of_records.get(record_id, default)

    def get_record_by_date(self, record_date: datetime, default = None):
        id_of_date = self._id_date_relation_dict.get(record_date)
        # returns None even if id_of_date is None
        return self.dict_of_records.get(id_of_date, default)

    def get_date_for_given_id(self, given_id: int, default = None):
        return self._id_date_relation_dict.get(given_id, default)

    def get_id_for_given_date(self, given_date: datetime, default = None):
        return self._id_date_relation_dict.get(given_date, default)
