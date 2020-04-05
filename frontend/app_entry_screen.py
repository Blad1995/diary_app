from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

from frontend.register_owner import RegisterOwner


class AppEntryScreen(GridLayout):
    def __init__(self, **kwargs):
        super(AppEntryScreen, self).__init__(**kwargs)
        self.cols = 1
        self.add_widget(Label(text="Welcome in the Diary App:"))

        self.add_widget(Button())


class MyApp(App):
    def build(self):
        return RegisterOwner()


if __name__ == "__main__":
    MyApp().run()
