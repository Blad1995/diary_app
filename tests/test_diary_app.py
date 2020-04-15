import logging as log
import os
import sys
from unittest import TestCase

from backend_scripts.diary_owner import Owner, OwnerInfo
from diary_app import DiaryControl

# TEST CONSTANTS
LOGIN1 = "BladM7#2→"
PASSWORD1 = "pswd→☼♂"
LOGIN2 = "Lgoinasdasd"
PASSWORD2 = "98as987a987"


class TestDiaryControl(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestDiaryControl, self).__init__(*args, **kwargs)
        log.basicConfig(level=log.DEBUG)
        for test_path in sys.path:
            if os.path.isfile(test_path + "/config.yml"):
                self.conf_path = test_path

    def test_owners(self):
        test_diary_control = DiaryControl(self.conf_path)
        test_diary_control.create_owner(login=LOGIN1, password=PASSWORD1)
        test_owners = test_diary_control.owners
        self.assertEqual(test_owners.__len__(), 1)
        self.assertIsInstance(test_owners, list)
        self.assertIsInstance(test_owners[0], Owner)

    def test_owners_info(self):
        test_diary_control = DiaryControl(self.conf_path)
        test_diary_control.create_owner(login=LOGIN1, password=PASSWORD1)
        test_owners = test_diary_control.owners
        test_owners_info = test_diary_control.owners_info
        self.assertEqual(test_owners_info.__len__(), 1)
        self.assertIsInstance(test_owners_info, list)
        self.assertIsInstance(test_owners_info[0], OwnerInfo)
        self.assertIs(test_owners[0].info, test_owners_info[0])

    def test_create_owner(self):
        test_diary_control = DiaryControl(self.conf_path)

        test_diary_control.create_owner(login=LOGIN1, password=PASSWORD1)
        self.assertEqual(test_diary_control.owners[0].login, LOGIN1)
        self.assertTrue(test_diary_control.owners[0].is_password_valid(PASSWORD1))
        self.assertIsNone(test_diary_control.owners[0].name)

        test_diary_control.create_owner(login=LOGIN1,
                                        password=PASSWORD1,
                                        name="Ondra",
                                        bio="987654659874")
        test_owners = test_diary_control.owners
        self.assertEqual(test_owners.__len__(), 2)

    def test_delete_owner_by_login(self):
        test_diary_control = DiaryControl(self.conf_path)
        test_diary_control.create_owner(login=LOGIN1, password=PASSWORD1)
        test_diary_control.create_owner(login=LOGIN2,
                                        password=PASSWORD2)
        test_diary_control.delete_owner_by_login(del_login=LOGIN1)
        self.assertEqual(test_diary_control.owners.__len__(), 1)
        self.assertIsNone(test_diary_control.get_owner_by_login(LOGIN1))

        self.assertRaises(ValueError, test_diary_control.delete_owner_by_login, LOGIN1)
        self.assertRaises(ValueError, test_diary_control.delete_owner_by_login, None)

    def test_save_owners_to_disc(self):
        test_diary_control = DiaryControl(self.conf_path)
        test_diary_control.create_owner(login=LOGIN1, password=PASSWORD1)
        test_diary_control.create_owner(login=LOGIN2,
                                        password=PASSWORD2)
        test_diary_control.save_owners_to_disc()
        # TODO testy

    def test_save_owners_info_to_disc(self):
        self.fail()

    def test_save_data_to_disc(self):
        self.fail()

    def test_load_all_data_from_disc(self):
        self.fail()

    def test_set_config_first_use_false(self):
        self.fail()

    def test_get_owner_by_login(self):
        self.fail()

    def test_load_owners_info_from_disk(self):
        self.fail()

    def test_load_owner_from_disk(self):
        self.fail()

    def test_update_owner_info_list(self):
        self.assertRaises(NotImplementedError, DiaryControl(self.conf_path).update_owner_info_list)

    def test_erase_data_files(self):
        self.fail()
