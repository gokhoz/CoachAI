
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDIconButton
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, RoundedRectangle
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = (0.95, 0.95, 0.95, 1)

        self.layout = MDBoxLayout(orientation='vertical')
        self.add_widget(self.layout)

        menu_items = [
            {"text": "Enter Stats", "viewclass": "OneLineListItem", "on_release": lambda: self.navigate_to("stats_entry")},
            {"text": "Player List", "viewclass": "OneLineListItem", "on_release": lambda: self.navigate_to("player_list")},
            {"text": "Add Player", "viewclass": "OneLineListItem", "on_release": lambda: self.navigate_to("add_player")},
            {"text": "Half Court Zones", "viewclass": "OneLineListItem", "on_release": self.feature_coming_soon},
        ]
        self.menu = MDDropdownMenu(items=menu_items, width_mult=4)

        self.toolbar = MDTopAppBar(
            title="CoachAI Chat",
            elevation=4,
            pos_hint={"top": 1},
            md_bg_color=(0.16, 0.18, 0.22, 1),  # Header rengi
            specific_text_color=(1, 1, 1, 1),
            right_action_items=[["dots-vertical", lambda x: self.open_menu(x)]]
        )
        self.layout.add_widget(self.toolbar)

        self.chat_scroll = MDScrollView()
        self.chat_box = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=dp(8),
            padding=dp(10)
        )
        self.chat_box.bind(minimum_height=self.chat_box.setter('height'))
        self.chat_scroll.add_widget(self.chat_box)
        self.layout.add_widget(self.chat_scroll)

        self.input_bar = MDBoxLayout(orientation='horizontal', padding=dp(10), size_hint_y=None, height=dp(60), spacing=dp(10))
        self.user_input = MDTextField(
            hint_text="Type your message...",
            mode="rectangle",
            size_hint_x=0.85
        )
        self.user_input.bind(on_text_validate=self.send_message)
        self.send_button = MDIconButton(icon="send", on_release=self.send_message)
        self.input_bar.add_widget(self.user_input)
        self.input_bar.add_widget(self.send_button)
        self.layout.add_widget(self.input_bar)

    def open_menu(self, button):
        self.menu.caller = button
        self.menu.open()

    def navigate_to(self, screen_name):
        self.menu.dismiss()
        self.manager.transition.direction = 'left'
        self.manager.current = screen_name

    def feature_coming_soon(self, *args):
        self.menu.dismiss()
        from kivymd.toast import toast
        toast("This feature is not ready yet.")

    def send_message(self, instance=None):
        msg = self.user_input.text.strip()
        if not msg:
            return
        self.add_message("User: " + msg, sender="user")
        self.user_input.text = ""
        Clock.schedule_once(lambda dt: self.get_bot_response(msg), 0)

    def get_bot_response(self, msg):
        messages = [
            {"role": "system", "content": "You are CoachAI, a smart basketball assistant. Give helpful, motivating and context-aware answers to players and coaches."},
            {"role": "user", "content": msg}
        ]

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=150
            )
            reply = response["choices"][0]["message"]["content"].strip()
        except Exception as e:
            reply = f"CoachAI: ⚠️ Error: {str(e)}"

        self.add_message("CoachAI: " + reply, sender="bot")

    def add_message(self, text, sender):
        # Renkler
        if sender == "bot":
            bg_color = (0.16, 0.18, 0.22, 1)  # Header ile aynı
            text_color = (1, 1, 1, 1)
            halign = "left"
            radius = [dp(12), dp(12), dp(12), dp(0)]
            
        else:
            bg_color = (0.85, 0.92, 0.98, 1)  # Açık mavi
            text_color = (0, 0, 0, 1)
            halign = "right"
            radius = [dp(12), dp(12), dp(0), dp(12)]  

        label = MDLabel(
            text=text,
            font_size="16sp",
            halign=halign,
            theme_text_color="Custom",
            text_color=text_color,            
            size_hint=(1, None),
            padding=(dp(12), dp(8))
        )
        label.bind(texture_size=lambda instance, size: setattr(label, "height", size[1] + dp(10)))

        with label.canvas.before:
            Color(*bg_color)
            label.bg_rect = RoundedRectangle(pos=label.pos, size=label.size, radius=radius)

        def update_bg_rect(*_):
            label.bg_rect.pos = label.pos
            label.bg_rect.size = label.size

        label.bind(pos=update_bg_rect, size=update_bg_rect)

        self.chat_box.add_widget(label)
    
    def on_enter(self):
        if not hasattr(self, "greeted"):
            self.greeted = True
            self.add_message("Hello! I'm CoachAI! \nAsk me anything about basketball or your team.", "bot")
        
