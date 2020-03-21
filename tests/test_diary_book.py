import unittest as ut
from datetime import datetime
from os import path

from config import DiaryConfig
from diary_book import Diary


class TestDiary(ut.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestDiary, self).__init__(*args, **kwargs)
        DiaryConfig.load("../")

    def test_delete_record(self):
        self.fail()

    def test_create_record(self):
        self.fail()

    def test_update_record(self):
        self.fail()

    def test_export_to_txt(self):
        # TEST 1 - empty Diary
        test_diary = Diary(title="my title", bio="Můj první deníček")
        test_diary.export_to_txt("export")
        self.assertTrue(path.isfile(f"export/{test_diary.title.lower()}_{test_diary.date_of_creation.strftime(test_diary.cfg.date_format)}.txt"))

        # TEST 2 - Diary with record
        test_diary = Diary(title="my title", bio="Můj první deníček")
        test_diary.create_record(date_of_record=datetime(2000, 12, 1), title="myTitle", text="whatever\nsomething")
        test_diary.export_to_txt("export")
        self.assertTrue(path.isfile(f"export/{test_diary.title.lower()}_{test_diary.date_of_creation.strftime(test_diary.cfg.date_format)}.txt"))
