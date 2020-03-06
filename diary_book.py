import logging as log
import os as os
from datetime import datetime

# my modules
from config import DiaryConfig


class Diary:
    cfg = DiaryConfig

    def __init__(self, title: str, date_of_creation: datetime = None, list_of_records: dict = None, bio: str = None):
        self.title = title
        self.date_of_creation = date_of_creation if date_of_creation else datetime.today()
        self.list_of_records = list_of_records if list_of_records else []
        self.bio = bio
        self.list_of_removed_records = []
        log.info(datetime.now().strftime(f"{Diary.cfg.log_time_format} - ") + f"Diary was created {str(self)}")

    def __str__(self):
        date_str = self.date_of_creation.strftime("%d. %m. %Y")
        string = f"Title: {self.title} created on {date_str}"
        return string

    def delete_record(self, record_id: int):
        for record in self.list_of_records:
            if record['id'] == record_id:
                self.list_of_records.pop()

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
                        'records': self.list_of_records
                        })
                f.write(payload)
        except IOError as e:
            log.error(datetime.now().strftime(f"{Diary.cfg.log_time_format} - ") + f"Error writing to {file_path}. {e}")
            raise e
