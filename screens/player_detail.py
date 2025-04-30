
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.toolbar import MDTopAppBar
from kivy.metrics import dp
from database import get_player_stats

class PlayerDetailScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = MDBoxLayout(orientation="vertical")
        self.add_widget(self.layout)

        self.toolbar = MDTopAppBar(
            title="Player Stats",
            elevation=4,
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
            md_bg_color=(0.16, 0.18, 0.22, 1),
            specific_text_color=(1, 1, 1, 1)
        )
        self.layout.add_widget(self.toolbar)

        self.scroll = MDScrollView()
        self.content = MDBoxLayout(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(10),
            size_hint_y=None
        )
        self.content.bind(minimum_height=self.content.setter("height"))
        self.scroll.add_widget(self.content)
        self.layout.add_widget(self.scroll)

    def go_back(self):
        self.manager.transition.direction = "right"
        self.manager.current = "player_list"

    def display_player(self, player_data):
        self.content.clear_widgets()
        player_name = player_data["name"]
        player_id = player_data["id"]

        header = MDLabel(
            text=f"[b]{player_name}[/b]",
            markup=True,
            halign="center",
            font_style="H6",
            size_hint_y=None,
            height=dp(40)
        )
        self.content.add_widget(header)

        stats = get_player_stats(player_id)
        if not stats:
            self.content.add_widget(MDLabel(text="No stats available.", halign="center", size_hint_y=None, height=dp(30)))
            return

        for stat in stats:
            card = MDBoxLayout(
                orientation="vertical",
                padding=dp(12),
                spacing=dp(6),
                size_hint_y=None,
                height=dp(140),
                md_bg_color=(0.9, 0.93, 0.96, 1),
                radius=[dp(12)]
            )
            card.add_widget(MDLabel(text=f"Date: {stat[2]}", theme_text_color="Primary"))
            card.add_widget(MDLabel(text=f"Minutes: {stat[3]}  |  Points: {stat[4]}", theme_text_color="Secondary"))
            card.add_widget(MDLabel(text=f"Assists: {stat[5]}  |  Rebounds: {stat[6]}", theme_text_color="Secondary"))
            card.add_widget(MDLabel(text=f"Steals: {stat[7]}  |  Blocks: {stat[8]}", theme_text_color="Secondary"))
            self.content.add_widget(card)
