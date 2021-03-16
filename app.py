import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from sdk import SpaceTraders


class ConnectPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.rows = 4

        self.add_widget(Label(
            text = '[color=20dd20]Space Traders[/color]',
            height=Window.size[1] * 0.425,
            size_hint_y = None,
            font_size=30,
            markup=True
        ))

        connect_form = GridLayout(cols=2)

        connect_form.add_widget(Label(
            text='[color=20dd20]Username:[/color]',
            height=Window.size[1] * 0.05,
            size_hint_y = None,
            markup=True
        ))
        self.username = TextInput(
            height=Window.size[1] * 0.05,
            size_hint_y = None,
            multiline=False
        )
        connect_form.add_widget(self.username)

        connect_form.add_widget(Label(
            text='[color=20dd20]Token:[/color]',
            height=Window.size[1] * 0.05,
            size_hint_y = None,
            markup=True
        ))
        self.token = TextInput(
            height=Window.size[1] * 0.05,
            size_hint_y = None,
            multiline=False
        )
        connect_form.add_widget(self.token)

        connect_form.add_widget(Label(
            height=Window.size[1] * 0.05,
            size_hint_y = None
        ))
        self.submit = Button(
            text='Submit',
            height=Window.size[1] * 0.05,
            size_hint_y = None
        )
        self.submit.bind(on_press=self.submit_button)
        connect_form.add_widget(self.submit)

        self.add_widget(connect_form)
        self.add_widget(Label(
            height=Window.size[1] * 0.325,
            size_hint_y = None
        ))
        self.add_widget(Label(
            text = check_server_status(),
            height=Window.size[1] * 0.1,
            size_hint_y = None,
            font_size=30,
            markup=True
        ))

    def submit_button(self, instance):
        pass    


class SpaceTradersApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        self.connect_page = ConnectPage()
        screen = Screen(name='Connect')
        screen.add_widget(self.connect_page)
        self.screen_manager.add_widget(screen)

        return self.screen_manager


def check_server_status():
    server_status = SpaceTraders.get_status()
    if server_status['status_code'] == 200:
        return f'[color=20dd20]{server_status["response"]["status"]}[/color]'
    return '[color=20dd20]something is wrong[/color]'


if __name__ == '__main__':
    app = SpaceTradersApp()
    app.run()
