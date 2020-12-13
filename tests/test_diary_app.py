import logging as log
import os
import shutil
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

        test_diary_control.create_owner(login=LOGIN2,
                                        password=PASSWORD2,
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
        owners_path = list(map(lambda x: os.path.join(DiaryControl.cfg.dir_path, x) + DiaryControl.cfg.data_extension,
                               [LOGIN1, LOGIN2]))
        for file_path_full in owners_path:
            self.assertTrue(os.path.exists(file_path_full))
            os.remove(file_path_full)

    def test_save_owners_info_to_disc(self):
        test_diary_control = DiaryControl(self.conf_path)
        test_diary_control.create_owner(login=LOGIN1, password=PASSWORD1)
        test_diary_control.create_owner(login=LOGIN2,
                                        password=PASSWORD2)
        test_diary_control.save_owners_info_to_disc()
        owners_path = os.path.join(DiaryControl.cfg.dir_path, DiaryControl.cfg.owner_credentials_file_name)
        self.assertTrue(os.path.exists(owners_path))
        os.remove(owners_path)

    def test_load_all_data_from_disc(self):
        load_diary_control = DiaryControl(self.conf_path)
        self.assertRaises(RuntimeError, load_diary_control.load_all_data_from_disc)
        test_diary_control = DiaryControl(self.conf_path)
        test_diary_control.create_owner(login=LOGIN1, password=PASSWORD1)
        test_diary_control.create_owner(login=LOGIN2,
                                        password=PASSWORD2)
        test_diary_control.save_data_to_disc()
        load_diary_control.load_all_data_from_disc()
        self.assertEqual(load_diary_control.owners.__len__(), 2)
        self.assertIsInstance(load_diary_control.owners[-1], Owner)

        shutil.rmtree(DiaryControl.cfg.dir_path, ignore_errors=True)

    def test_get_owner_by_login(self):
        test_diary_control = DiaryControl(self.conf_path)
        test_diary_control.create_owner(login=LOGIN1, password=PASSWORD1)
        test_diary_control.create_owner(login=LOGIN2,
                                        password=PASSWORD2)
        self.assertIsNone(test_diary_control.get_owner_by_login("NotValid"))
        self.assertEqual(test_diary_control.get_owner_by_login("NotValid", "default"), "default")
        self.assertIsInstance(test_diary_control.get_owner_by_login(LOGIN1), Owner)
        # Not consistent - order of the owners in list is not guaranteed
        self.assertIs(test_diary_control.get_owner_by_login(LOGIN1), test_diary_control.owners[0])

    def test_load_owners_info_from_disk(self):
        load_diary_control = DiaryControl(self.conf_path)
        self.assertRaises(RuntimeError, load_diary_control.load_owners_info_from_disc)

        test_diary_control = DiaryControl(self.conf_path)
        test_diary_control.create_owner(login=LOGIN1, password=PASSWORD1)
        test_diary_control.create_owner(login=LOGIN2,
                                        password=PASSWORD2)
        test_diary_control.save_owners_info_to_disc()

        loaded_owner_info = load_diary_control.load_owners_info_from_disc()
        self.assertIsInstance(loaded_owner_info, list)
        self.assertTrue(OwnerInfo(login=LOGIN1, password="") in loaded_owner_info)
        os.remove(os.path.join(DiaryControl.cfg.dir_path, DiaryControl.cfg.owner_credentials_file_name))

    def test_load_owner_from_disk(self):
        test_diary_control = DiaryControl(self.conf_path)
        test_diary_control.create_owner(login=LOGIN1, password=PASSWORD1)
        test_diary_control.create_owner(login=LOGIN2,
                                        password=PASSWORD2)
        test_diary_control.save_owners_to_disc()

        owners = []
        for login_str in [LOGIN1, LOGIN2]:
            owners.append(test_diary_control.load_owner_from_disc(login_str))
            self.assertIsInstance(owners[-1], Owner)
            self.assertEqual(owners[-1].login, login_str)
            self.assertIsNone(owners[-1].name)
            test_diary_control.erase_owner_data_files(login_str)

        # TODO load of more complex owner structure

    def test_update_owner_info_list(self):
        self.assertRaises(NotImplementedError, DiaryControl(self.conf_path).update_owner_info_list)

    def test_erase_data_files(self):
        test_diary_control = DiaryControl(self.conf_path)
        test_diary_control.create_owner(login=LOGIN1, password=PASSWORD1)
        test_diary_control.create_owner(login=LOGIN2,
                                        password=PASSWORD2)
        test_diary_control.save_owners_to_disc()
        owners_path = list(map(lambda x: os.path.join(DiaryControl.cfg.dir_path, x) + DiaryControl.cfg.data_extension,
                               [LOGIN1, LOGIN2]))
        for login_str, file_path_full in zip([LOGIN1, LOGIN2], owners_path):
            test_diary_control.erase_owner_data_files(login_str)
            self.assertFalse(os.path.exists(file_path_full))
