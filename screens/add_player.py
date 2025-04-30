from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.toast import toast
from kivy.metrics import dp
from kivymd.uix.toolbar import MDTopAppBar
import database  # <-- EKLENDİ

class AddPlayerScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        self.toolbar = MDTopAppBar(
            title="Add Player",
            pos_hint={"top": 1},
            elevation=4,
            md_bg_color=(0.16, 0.18, 0.22, 1),
            specific_text_color=(1, 1, 1, 1),
            left_action_items=[["arrow-left", lambda x: self.go_back()]]
        )
        self.add_widget(self.toolbar)

        self.name_input = MDTextField(hint_text="Name")
        self.surname_input = MDTextField(hint_text="Surname")
        self.position_input = MDTextField(hint_text="Position")
        self.number_input = MDTextField(hint_text="Jersey Number", input_filter="int")

        self.save_button = MDRaisedButton(
            text="Add Player",
            pos_hint={"center_x": 0.5},
            on_release=self.save_player
        )

        layout.add_widget(self.name_input)
        layout.add_widget(self.surname_input)
        layout.add_widget(self.position_input)
        layout.add_widget(self.number_input)
        layout.add_widget(self.save_button)

        self.add_widget(layout)

    def go_back(self):
        self.manager.transition.direction = "right"
        self.manager.current = "home"

    def save_player(self, *args):
        name = self.name_input.text.strip()
        surname = self.surname_input.text.strip()
        position = self.position_input.text.strip()
        number = self.number_input.text.strip()

        if not all([name, surname, position, number]):
            toast("Please fill all fields.")
            return

        full_name = f"{name} {surname}"
        database.add_player(full_name, int(number), position)  # <-- EKLENDİ
        toast(f"{full_name} added!")

        self.name_input.text = ""
        self.surname_input.text = ""
        self.position_input.text = ""
        self.number_input.text = ""
