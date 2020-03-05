from datetime import date


class Diary:

    def __init__(self, title: str, date_of_creation: str = None, list_of_records: dict = None, bio: str = None):
        self.title = title
        self.date_of_creation = date_of_creation if date_of_creation else date.today().strftime("%d. %m. %Y")
        self.list_of_records = list_of_records if list_of_records else []
        self.bio = bio
        self.list_of_removed_records = []

    def delete_record(self, record_id: int):
        for record in self.list_of_records:
            if record['id'] == record_id:
                self.list_of_records.pop()

    def export(self, destination):
        with open(f'{self.title.lower()}_{self.date_of_creation}.txt', 'w') as f:
            payload = str(
                {
                    'title': self.title,
                    'date_of_creation': self.date_of_creation,
                    'bio': self.bio,
                    'records': self.list_of_records
                    })
            f.write(payload)
