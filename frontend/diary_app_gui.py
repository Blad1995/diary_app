from kivy import require as kivy_require
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import FadeTransition, Screen, ScreenManager

from diary_app import DiaryControl

kivy_require('1.11.1')
Window.size = (800, 600)
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


class LoginWindow(Screen):
    def check_login_validity(self, input_login: str, input_password: str):
        app = App.get_running_app()
        if login_exists(input_login):
            o_info = app.diary_ctr.get_owner_info_by_login(input_login)
            if o_info.is_password_valid(input_password):
                # If valid, proceed to next level
                self.change_screen(new_screen="W_MainWindow")
            else:
                wrong_password_popup = Popup(content=Label(text="Password is not valid"))
                wrong_password_popup.open()
                # When popup disappear change the screen
                wrong_password_popup.bind(on_dismiss=lambda *args: change_screen(self))
        else:
            wrong_login_popup = Popup(content=Label(text="Login doesn't exist"),
                                      title="Login error",
                                      size_hint=(None, None),
                                      size=(200, 100))
            wrong_login_popup.open()
            # When popup disappear change the screen
            wrong_login_popup.bind(on_dismiss=lambda *args: change_screen(self))


class CreateUserWindow(Screen):
    def on_leave(self, *args):
        # Erase text in all TextInput fields
        self.ids.get("ti_new_login").text = ""
        self.ids.get("ti_new_password").text = ""
        self.ids.get("ti_new_password_confirm").text = ""
        self.ids.get("ti_new_owner_name").text = ""
        self.ids.get("ti_new_owner_email").text = ""
        self.ids.get("ti_new_owner_bio").text = ""

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
        result = self.check_duplicate_login(self.ids.get("ti_new_login").text) and \
                 self.check_password_confirm(self.ids.get("ti_new_password").text,
                                             self.ids.get("ti_new_password_confirm").text)
        return result

    def create_user(self):
        diary: DiaryControl = App.get_running_app().diary_ctr
        diary.create_owner(
            login=self.ids.get("ti_new_login").text,
            password=self.ids.get("ti_new_password").text,
            name=self.ids.get("ti_new_owner_name").text,
            email=self.ids.get("ti_new_owner_email").text,
            bio=self.ids.get("ti_new_owner_bio").text
            )


app_builder = Builder.load_file("diary_app_design.kv")


class DiaryAppGUI(App):
    diary_ctr = DiaryControl("../")

    def build(self):
        return app_builder

    def on_start(self):
        if not self.diary_ctr.cfg.first_use:
            self.diary_ctr.load_owners_info_from_disc()

    def on_stop(self):
        self.diary_ctr.cfg.save()


if __name__ == "__main__":
    DiaryAppGUI().run()
