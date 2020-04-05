class RegisterOwner(GridLayout):
    def __init__(self, **kwargs):
        super(RegisterOwner, self).__init__(**kwargs)
        self.cols = 1

        # New layout for title
        self.title_layout = GridLayout()
        self.title_layout.cols = 1
        self.title_layout.add_widget(Label(text="Please fill all information required (*)"))

        # Layout for rest of screen
        self.rest_layout = GridLayout()
        self.rest_layout.cols = 2

        # Login row
        self.rest_layout.add_widget(Label(text="*Login:"))
        self.TI_login = TextInput(multiline=False)
        self.rest_layout.add_widget(self.TI_login)

        # Password row
        self.rest_layout.add_widget(Label(text="*Password:"))
        self.TI_password = TextInput(multiline=False)
        self.rest_layout.add_widget(self.TI_password)

        # Cancel button
        self.BT_cancel = Button(text="Cancel")
        self.rest_layout.add_widget(self.BT_cancel)
        self.BT_cancel.bind(on_press=self.exit_app)

        # Confirm button
        self.BT_confirm = Button(text="Confirm")
        self.rest_layout.add_widget(self.BT_confirm)
        self.BT_confirm.bind(on_press=self.confirm_registration)

        # add both layouts into one
        self.add_widget(self.title_layout)
        self.add_widget(self.rest_layout)

    def exit_app(self, instance):
        exit(10)

    def confirm_registration(self, instance):
        print(self.TI_login.text + " " + self.TI_password.text)
