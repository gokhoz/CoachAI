from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.card import MDCard
from kivy.metrics import dp
from database import get_all_players

class PlayerListScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.md_bg_color = (0.69, 0.745, 0.77, 1)  

        self.layout = MDBoxLayout(orientation='vertical')
        self.add_widget(self.layout)

        # Header
        self.toolbar = MDTopAppBar(
            title="Player List",
            elevation=4,
            pos_hint={"top": 1},
            md_bg_color=(0.16, 0.18, 0.22, 1),
            left_action_items=[["arrow-left", lambda x: self.go_back()]]
        )
        self.layout.add_widget(self.toolbar)

        # Scrollable Player List
        self.scroll = MDScrollView()
        self.list_container = MDBoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10), size_hint_y=None)
        self.list_container.bind(minimum_height=self.list_container.setter('height'))
        self.scroll.add_widget(self.list_container)
        self.layout.add_widget(self.scroll)

        # Load players
        self.load_players()

    def load_players(self):
        self.list_container.clear_widgets()
        players = get_all_players()

        for player in players:
            card = MDCard(
                orientation='vertical',
                padding=dp(10),
                size_hint=(1, None),
                height=dp(80),
                md_bg_color=(1, 1, 1, 1),
                ripple_behavior=True,
                on_release=lambda x, pid=player[0], name=player[1]: self.open_player(pid, name)
            )
            label = MDLabel(
                text=f"{player[1]}  •  #{player[2]}  •  {player[3]}",
                font_style="Subtitle1",
                halign="left"
            )
            card.add_widget(label)
            self.list_container.add_widget(card)

    def go_back(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'home'

    def open_player(self, player_id, name):
        detail_screen = self.manager.get_screen("player_detail")
        detail_screen.display_player({"id": player_id, "name": name})
        self.manager.transition.direction = "left"
        self.manager.current = "player_detail"

    def on_pre_enter(self):
        self.load_players()
