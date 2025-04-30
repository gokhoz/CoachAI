from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

def create_header(screen, title_text):
    header = BoxLayout(
        orientation='horizontal',
        size_hint=(1, None),
        height=40,
        padding=(5, 5),
        spacing=10
    )

    back_btn = Button(
        text='← Back',
        size_hint=(None, 1),
        font_name='EmojiFont',
        width=80
    )
    back_btn.bind(on_press=lambda instance: switch_to(screen, 'home', direction='right'))


    title = Label(
        text=title_text,
        halign='center',
        valign='middle'
    )

    header.add_widget(back_btn)
    header.add_widget(title)

    return header

def switch_to(screen, screenname, direction='left'):
    screen.manager.transition.direction = direction
    screen.manager.current = screenname