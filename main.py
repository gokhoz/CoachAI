from kivy.config import Config
Config.set('graphics', 'width', '450')
Config.set('graphics', 'height', '800')
Config.set('graphics', 'resizable', False)
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition, NoTransition
from screens.home import HomeScreen
from kivy.core.text import LabelBase
from kivymd.app import MDApp
from screens.player_list import PlayerListScreen
from screens.add_player import AddPlayerScreen
from screens.player_detail import PlayerDetailScreen
from screens.stats_entry import StatsEntryScreen

from database import init_db
init_db()

# Özel fontu kaydet
LabelBase.register(
    name='EmojiFont',
    fn_regular='assets/fonts/Symbola.ttf'
)

class CoachAIApp(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        return sm
    def build(self):
        sm = ScreenManager(transition=SlideTransition(direction= 'left'))
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(PlayerListScreen(name='player_list')) 
        sm.add_widget(AddPlayerScreen(name='add_player'))
        sm.add_widget(PlayerDetailScreen(name='player_detail'))
        sm.add_widget(StatsEntryScreen(name='stats_entry')) # ← bu satırı ekle
        return sm

if __name__ == '__main__':
    CoachAIApp().run()