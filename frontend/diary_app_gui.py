from kivy import require as kivy_require
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import FadeTransition, Screen, ScreenManager
# noinspection PyUnresolvedReferences
from KivyCalendar import DatePicker, CalendarWidget

from diary_app import DiaryControl
from backend_scripts.diary_owner import Owner
from backend_scripts.diary_book import Diary
from backend_scripts.diary_record import DiaryRecord

kivy_require('1.11.1')
Window.size = (1280, 800)
Window.minimum_width, Window.minimum_height = (600, 450)


def change_screen(screen_instance: Screen, new_screen: str = "W_Entry"):
    screen_instance.manager.current = new_screen


def login_exists(login: str):
    return App.get_running_app().diary_ctr.login_exists(login=login)


class WindowManager(ScreenManager):
    def __init__(self, **kwargs):
        super(WindowManager, self).__init__(**kwargs, transition=FadeTransition(duration=0.2))


class EntryWindow(Screen):
    pass


class DiaryPickWindow(Screen):
    def on_enter(self, *args):
        app: DiaryAppGUI = App.get_running_app()
        if app.current_owner:
            diaries = app.current_owner.dict_of_diaries
        else:
            raise RuntimeError("No diary chosen. Invalid sequence of steps.")
        for title, diary in diaries:
            print(f"Diary named {title}")


class DatePickWindow(Screen):
    pass


class LoginWindow(Screen):
    def on_pre_leave(self, *args):
        self.ids.get("ti_wlogin_login").text = ""
        self.ids.get("ti_wlogin_password").text = ""

    def check_login_validity(self, input_login: str, input_password: str):
        app = App.get_running_app()
        if login_exists(input_login):
            o_info = app.diary_ctr.get_owner_info_by_login(input_login)
            if o_info.is_password_valid(input_password):
                # If valid, proceed to next level
                app.current_owner = app.diary_ctr.get_owner_by_login(login=o_info.login)
                change_screen(self, new_screen="W_DiaryPick")
            else:
                wrong_password_popup = Popup(content=Label(text="Password is not valid"),
                                             title="Login error",
                                             size_hint=(None, None),
                                             size=(200, 100)
                                             )
                wrong_password_popup.open()
                # When popup disappear change the screen
                wrong_password_popup.bind(on_dismiss=lambda *args: change_screen(screen_instance=self,
                                                                                 new_screen="W_Login"))
        else:
            wrong_login_popup = Popup(content=Label(text="Login doesn't exist"),
                                      title="Login error",
                                      size_hint=(None, None),
                                      size=(200, 100))
            wrong_login_popup.open()
            # When popup disappear change the screen
            wrong_login_popup.bind(on_dismiss=lambda *args: change_screen(screen_instance=self,
                                                                          new_screen="W_Entry"))


class CreateUserWindow(Screen):
    def on_leave(self, *args):
        # Erase text in all TextInput fields
        self.ids.get("ti_wcreateuser_login").text = ""
        self.ids.get("ti_wcreateuser_password").text = ""
        self.ids.get("ti_wcreateuser_password_confirm").text = ""
        self.ids.get("ti_wcreateuser_name").text = ""
        self.ids.get("ti_wcreateuser_email").text = ""
        self.ids.get("ti_wcreateuser_bio").text = ""

    def check_duplicate_login(self, login):
        if login_exists(login=login):
            wrong_login_popup = Popup(content=Label(text="Login already exists"),
                                      title="Login exists",
                                      size_hint=(None, None),
                                      size=(400, 200))
            wrong_login_popup.open()
            # When popup disappear change the screen to Entry
            wrong_login_popup.bind(on_dismiss=lambda *args: change_screen(self, "W_Login"))
            return False
        else:
            return True

    def check_password_confirm(self, password: str, password_confirm: str):
        if password != password_confirm:
            wrong_login_popup = Popup(content=Label(text="Passwords are not the same"),
                                      title="Wrong password",
                                      size_hint=(None, None),
                                      size=(400, 200))
            wrong_login_popup.open()
            # When popup disappear change the screen to Entry
            wrong_login_popup.bind(on_dismiss=lambda *args: change_screen(self, "W_CreateUser"))
            return False
        else:
            return True

    def perform_check(self):
        # TODO short password or empty login
        result = self.check_duplicate_login(self.ids.get("ti_wcreateuser_login").text) and \
                 self.check_password_confirm(self.ids.get("ti_wcreateuser_password").text,
                                             self.ids.get("ti_wcreateuser_password_confirm").text)
        return result

    def create_user(self):
        diary: DiaryControl = App.get_running_app().diary_ctr
        diary.create_owner(
            login=self.ids.get("ti_wcreateuser_login").text,
            password=self.ids.get("ti_wcreateuser_password").text,
            name=self.ids.get("ti_wcreateuser_name").text,
            email=self.ids.get("ti_wcreateuser_email").text,
            bio=self.ids.get("ti_wcreateuser_bio").text
            )
        change_screen(screen_instance=self, new_screen="W_Entry")


class DiaryAppGUI(App):
    diary_ctr: DiaryControl = DiaryControl("../")

    def __init__(self, *args, **kwargs):
        super(DiaryAppGUI, self).__init__(*args, **kwargs)
        self.current_owner: Owner = None
        self.current_diary: Diary = None
        self.current_record: DiaryRecord = None

    def build(self):
        return Builder.load_file("diary_app_design.kv")

    def on_start(self):
        if not self.diary_ctr.cfg.first_use:
            self.diary_ctr.load_owners_info_from_disc()

    def on_stop(self):
        # self.diary_ctr.save_data_to_disc()
        self.diary_ctr.cfg.save()


if __name__ == "__main__":
    DiaryAppGUI().run()
