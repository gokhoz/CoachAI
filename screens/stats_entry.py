
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.toast import toast
from kivymd.uix.textfield import MDTextField
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.scrollview import MDScrollView
from kivy.metrics import dp
from datetime import datetime
import database

class StatsEntryScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_player = None
        self.menu = None

        main_layout = MDBoxLayout(orientation="vertical")

        self.toolbar = MDTopAppBar(
            title="Enter Stats",
            pos_hint={"top": 1},
            elevation=4,
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
            md_bg_color=(0.16, 0.18, 0.22, 1),
            specific_text_color=(1, 1, 1, 1)
        )
        main_layout.add_widget(self.toolbar)

        scroll = MDScrollView()
        form_layout = MDBoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(15),
            size_hint_y=None
        )
        form_layout.bind(minimum_height=form_layout.setter('height'))
        scroll.add_widget(form_layout)

        self.select_button = MDRaisedButton(
            text="Select Player",
            pos_hint={"center_x": 0.5},
            on_release=self.open_player_menu
        )

        self.minutes_input = MDTextField(hint_text="Minutes", input_filter="int")
        self.points_input = MDTextField(hint_text="Points", input_filter="int")
        self.assists_input = MDTextField(hint_text="Assists", input_filter="int")
        self.rebounds_input = MDTextField(hint_text="Rebounds", input_filter="int")
        self.steals_input = MDTextField(hint_text="Steals", input_filter="int")
        self.blocks_input = MDTextField(hint_text="Blocks", input_filter="int")

        self.save_button = MDRaisedButton(
            text="Save Stats",
            pos_hint={"center_x": 0.5},
            on_release=self.save_stats
        )

        for widget in [
            self.select_button, self.minutes_input, self.points_input, self.assists_input,
            self.rebounds_input, self.steals_input, self.blocks_input, self.save_button
        ]:
            form_layout.add_widget(widget)

        main_layout.add_widget(scroll)
        self.add_widget(main_layout)

    def go_back(self):
        self.manager.transition.direction = "right"
        self.manager.current = "home"

    def open_player_menu(self, instance):
        players = database.get_all_players()
        self.menu_items = [{
            "text": f"{p[1]} ({p[3]})",
            "viewclass": "OneLineListItem",
            "on_release": lambda x=p: self.select_and_close_menu(x)
        } for p in players]

        self.menu = MDDropdownMenu(
            caller=self.select_button,
            items=self.menu_items,
            width_mult=4
        )
        self.menu.open()

    def select_and_close_menu(self, player_tuple):
        self.selected_player = player_tuple
        self.select_button.text = f"{player_tuple[1]} ({player_tuple[3]})"
        self.menu.dismiss()

    def save_stats(self, *args):
        if not self.selected_player:
            toast("Please select a player.")
            return

        stat_data = {
            "date": datetime.today().strftime('%Y-%m-%d'),
            "minutes": int(self.minutes_input.text.strip() or 0),
            "points": int(self.points_input.text.strip() or 0),
            "assists": int(self.assists_input.text.strip() or 0),
            "rebounds": int(self.rebounds_input.text.strip() or 0),
            "steals": int(self.steals_input.text.strip() or 0),
            "blocks": int(self.blocks_input.text.strip() or 0)
        }

        database.insert_stat(self.selected_player[0], stat_data)
        toast(f"Stats saved for {self.selected_player[1]}")

        self.minutes_input.text = ""
        self.points_input.text = ""
        self.assists_input.text = ""
        self.rebounds_input.text = ""
        self.steals_input.text = ""
        self.blocks_input.text = ""
