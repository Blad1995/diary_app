import unittest as ut
from datetime import datetime
from os import path

from config import DiaryConfig
from diary_book import Diary
from diary_record import DiaryRecord


class TestDiary(ut.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestDiary, self).__init__(*args, **kwargs)
        DiaryConfig.load("../")

    def test_create_record(self):
        test_diary = Diary(title="title")
        test_diary.create_record(date_of_record=datetime(2000, 12, 1), title="myTitle", text="whatever\nsomething")
        # Creates good class object
        self.assertIsInstance(test_diary.dict_of_records[0], DiaryRecord)
        # Creates only one record
        self.assertRaises(KeyError, lambda x: test_diary.dict_of_records[x], 1)
        self.assertRaises(KeyError, lambda x: test_diary.dict_of_records[x], 2)

        self.assertRaises(AssertionError, test_diary.create_record, date_of_record=5, title="Ahoj", text="Ahoj")

        new_record: DiaryRecord = test_diary.dict_of_records.get(0, None)
        self.assertEqual(new_record.text, "whatever\nsomething")
        self.assertEqual(new_record.title, "myTitle")
        self.assertEqual(new_record.date, datetime(2000, 12, 1))

    def test_delete_record(self):
        test_diary = Diary(title="title")
        test_diary.create_record(date_of_record=datetime(2000, 12, 1), title="myTitle", text="whatever\nsomething")
        test_diary.create_record(date_of_record=datetime(2001, 12, 1), title="myTitle", text="whatever\nsomething")
        test_diary.create_record(date_of_record=datetime(2002, 12, 1), title="myTitle", text="whatever\nsomething")

        test_diary.delete_record(1)
        self.assertIsNone(test_diary.dict_of_records.get(1, None))
        self.assertIsNotNone(test_diary.dict_of_removed_records.get(1, None))
        self.assertIsNotNone(test_diary.dict_of_records.get(0, None))
        self.assertIsNotNone(test_diary.dict_of_records.get(2, None))

        self.assertRaises(ValueError, test_diary.delete_record, 10)
        self.assertRaises(ValueError, test_diary.delete_record, -5)

    def test_update_record(self):
        test_diary = Diary(title="title")
        test_diary.create_record(date_of_record=datetime(2000, 12, 1), title="myTitle", text="whatever\nsomething")
        test_diary.create_record(date_of_record=datetime(2001, 12, 1), title="myTitle", text="whatever\nsomething")
        test_diary.create_record(date_of_record=datetime(2002, 12, 1), title="myTitle", text="whatever\nsomething")

        test_diary.update_record(1, date_of_record=datetime(2019, 2, 1))
        # test only one information has changed
        self.assertEqual(test_diary.dict_of_records[1].date, datetime(2019, 2, 1))
        self.assertEqual(test_diary.dict_of_records[1].title, "myTitle")
        self.assertEqual(test_diary.dict_of_records[1].text, "whatever\nsomething")

        test_diary.update_record(2, date_of_record=datetime(2019, 2, 1), title="Ahoj")
        # test two information has changed
        self.assertEqual(test_diary.dict_of_records[2].date, datetime(2019, 2, 1))
        self.assertEqual(test_diary.dict_of_records[2].title, "Ahoj")
        self.assertEqual(test_diary.dict_of_records[2].text, "whatever\nsomething")

        test_diary.update_record(2, text="blbl")
        # test every information has changed
        self.assertEqual(test_diary.dict_of_records[2].date, datetime(2019, 2, 1))
        self.assertEqual(test_diary.dict_of_records[2].title, "Ahoj")
        self.assertEqual(test_diary.dict_of_records[2].text, "blbl")

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
