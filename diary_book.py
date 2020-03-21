import logging as log
import os as os
from datetime import datetime

# my modules
from config import DiaryConfig
from diary_record import DiaryRecord


class Diary:
    cfg = DiaryConfig

    def __init__(self, title: str, date_of_creation: datetime = None, dict_of_records: dict = None, bio: str = None):
        self.title = title
        self.date_of_creation = date_of_creation if date_of_creation else datetime.today()
        self.dict_of_records = dict_of_records if dict_of_records else {}
        self.bio = bio
        self.dict_of_removed_records = {}
        self.last_id: int = max(dict_of_records.keys()) if dict_of_records else 0
        log.info(datetime.now().strftime(f"{Diary.cfg.log_time_format} - ") + f"Diary was created {str(self)}")

    def __str__(self):
        date_str = self.date_of_creation.strftime("%d. %m. %Y")
        string = f"Title: {self.title} created on {date_str}"
        return string

    def delete_record(self, record_id: int):
        if record_id in self.dict_of_records:
            self.dict_of_removed_records.update(self.dict_of_records.pop(record_id))
        else:
            log.warning(datetime.now().strftime(f"{Diary.cfg.log_time_format} - ") + f"No such record with id = {record_id} in diary {str(self)}")

    def export_to_txt(self, destination: str):
        if not os.path.isdir(destination):
            raise FileNotFoundError(f"{destination} is not a valid directory.")
        file_path = destination.rstrip("/") + "/" + f'{self.title.lower()}_{self.date_of_creation}.txt'
        try:
            with open(file_path, 'w') as f:
                payload = str(
                    {
                        'title': self.title,
                        'date_of_creation': self.date_of_creation,
                        'bio': self.bio,
                        # TODO test if this str conversion works
                        'records': self.dict_of_records
                        })
                f.write(payload)
        except IOError as e:
            log.error(datetime.now().strftime(f"{Diary.cfg.log_time_format} - ") + f"Error writing to {file_path}. {e}")
            raise e

    def create_record(self, date_of_record: datetime, title: str, text: str, date_of_creation: datetime = None):
        assert type(date_of_record) == datetime
        assert type(title) == str
        assert type(text) == str

        self.last_id += 1
        if self.dict_of_records.get(self.last_id, None):
            # If record with this id already exist (it shouldn't) reset the counter
            self.last_id = max(self.dict_of_records.keys())
            log.warning(datetime.now().strftime(f"{Diary.cfg.log_time_format} - ") + f"id: {self.last_id} is already taken! last_id counter was reset")

        try:
            self.dict_of_records[self.last_id] = DiaryRecord(id=self.last_id, date=date_of_record, title=title, text=text, date_of_creation=date_of_creation)
        except Exception as e:
            log.error(datetime.now().strftime(f"{Diary.cfg.log_time_format} - ") + f"Unexpected error when creating the record in Diary. {e}")
            log.debug(f"Parameters of Diary.create_record: Title:{title}, date_of_record: {date_of_record}, text={text}")
            raise e

    def update_record(self):
        # TODO update
        pass
