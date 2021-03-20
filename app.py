import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock
from space_traders import SpaceTraders
from pathlib import Path
import logging
from datetime import datetime, timedelta


kivy.require('2.0.0')
text_color = [0, 1, 0, 1]


class User(object):
    def __init__(self, username=None):
        self.username = username
        self.user_info = None
        self.login_time = None


class ConnectPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.rows = 4

        if Path('user_details.txt').is_file():
            with open('user_details.txt', 'rt') as f:
                d = f.read().split(',')
            prev_username = d[0]
            prev_token=d[1]
        else:
            prev_username = ''
            prev_token = ''

        header = Label(
            text = 'Space Traders',
            height=Window.size[1] * 0.425,
            size_hint_y = None,
            font_size=30,
            color=text_color,
        )

        username_label = Label(
            text='Username:',
            height=Window.size[1] * 0.05,
            size_hint_y = None,
            color=text_color,
        )
        self.username = TextInput(
            text=prev_username,
            height=Window.size[1] * 0.05,
            size_hint_y = None,
            multiline=False,
        )
        token_label = Label(
            text='Token:',
            height=Window.size[1] * 0.05,
            size_hint_y = None,
            color=text_color,
        )
        self.token = TextInput(
            text=prev_token,
            height=Window.size[1] * 0.05,
            size_hint_y = None,
            multiline=False,
            password=True,
        )
        dummy_label_a = Label(
            height=Window.size[1] * 0.05,
            size_hint_y = None,
        )
        self.submit = Button(
            text='Submit',
            height=Window.size[1] * 0.05,
            size_hint_y = None,
        )
        self.submit.bind(on_press=self.submit_button)
        dummy_label_b = Label(
            height=Window.size[1] * 0.05,
            size_hint_y = None,
        )
        self.error_message = Label(
            height=Window.size[1] * 0.05,
            size_hint_y = None,
            color=text_color
        )

        footer = Label(
            height=Window.size[1] * 0.275,
            size_hint_y = None,
        )

        server_status = Label(
            text = check_server_status(),
            height=Window.size[1] * 0.1,
            size_hint_y = None,
            font_size=30,
            color=text_color,
        )

        connect_form = GridLayout(cols=2)

        connect_form.add_widget(username_label)
        connect_form.add_widget(self.username)
        connect_form.add_widget(token_label)
        connect_form.add_widget(self.token)
        connect_form.add_widget(dummy_label_a)
        connect_form.add_widget(self.submit)
        connect_form.add_widget(dummy_label_b)
        connect_form.add_widget(self.error_message)

        self.add_widget(header)
        self.add_widget(connect_form)
        self.add_widget(footer)
        self.add_widget(server_status)

    def submit_button(self, instance):
        if not self.username.text:
            self.error_message.text = 'Username is required.'
            logging.info('[Game        ] Username is required')
            return None
        s.username = self.username.text
        s.token = self.token.text
        if not s.token:
            generated_token = s.generate_token()
            if generated_token['status_code'] != 201:
                self.error_message.text = generated_token['response']['error']['message']
                logging.info(f'[Game        ] {generated_token["response"]["error"]["message"]}')
                return None
        user_info = s.get_user_info()
        if user_info['status_code'] != 200:
            self.error_message.text = generated_token['response']['error']['message']
            logging.info(f'[Game        ] {generated_token["response"]["error"]["message"]}')
            return None
        u.username = s.username
        u.user_info = user_info['response']['user']
        with open('user_details.txt', 'wt') as f:
            f.write(f'{s.username},{s.token}')
        Clock.schedule_once(self.log_in, 0.1)
        logging.info(f'[Game        ] {s.username} is logged in')

        
    def log_in(self, _):
        app.create_game_page()
        app.screen_manager.current = 'Game'


class GamePage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rows = 2

        header = Label(
            text=f'{u.username}    \u20B9 {u.user_info["credits"]}',
            height=Window.size[1] * 0.05,
            size_hint_y=None,
            color=text_color,
        )

        self.flight_plans = Button(
            text='Flight plans',
            width=Window.size[0] * 0.1,
            size_hint_x = None,
        )
        self.loans = Button(
            text='Loans',
            width=Window.size[0] * 0.1,
            size_hint_x = None,
        )
        self.locations = Button(
            text='Locations',
            width=Window.size[0] * 0.1,
            size_hint_x = None,
        )
        self.market = Button(
            text='Market',
            width=Window.size[0] * 0.1,
            size_hint_x = None,
        )
        self.ships = Button(
            text='Ships',
            width=Window.size[0] * 0.1,
            size_hint_x = None,
        )
        dummy_label = Label(
            height=Window.size[1] * 0.75,
            size_hint_y=None,
            color=text_color,
        )
        self.flight_plans.bind(on_press=self.flight_plans_button)
        self.loans.bind(on_press=self.loans_button)
        self.locations.bind(on_press=self.locations_button)
        self.market.bind(on_press=self.market_button)
        self.ships.bind(on_press=self.ships_button)

        self.main_content_label = Label(
            text=f'Welcome, {u.username}',
            width=Window.size[0] * 0.9,
            size_hint_x = None,
            color=text_color,
        )

        main_content = GridLayout(cols=2)
        sidebar = GridLayout(rows=6)

        sidebar.add_widget(self.flight_plans)
        sidebar.add_widget(self.loans)
        sidebar.add_widget(self.locations)
        sidebar.add_widget(self.market)
        sidebar.add_widget(self.ships)
        sidebar.add_widget(dummy_label)

        main_content.add_widget(sidebar)
        main_content.add_widget(self.main_content_label)

        self.add_widget(header)
        self.add_widget(main_content)

    def flight_plans_button(self, instance):
        self.main_content_label.text = 'Flight plans'

    def loans_button(self, instance):
        self.main_content_label.text = 'Loans'

    def locations_button(self, instance):
        self.main_content_label.text = 'Locations'

    def market_button(self, instance):
        self.main_content_label.text = 'Market'

    def ships_button(self, instance):
        self.main_content_label.text = 'Ships'



class SpaceTradersApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        self.connect_page = ConnectPage()
        screen = Screen(name='Connect')
        screen.add_widget(self.connect_page)
        self.screen_manager.add_widget(screen)

        return self.screen_manager

    def create_game_page(self):
        self.game_page = GamePage()
        screen = Screen(name='Game')
        screen.add_widget(self.game_page)
        self.screen_manager.add_widget(screen)


def check_server_status():
    server_status = SpaceTraders.get_status()
    if server_status['status_code'] == 200:
        return f'{server_status["response"]["status"]}'
    return 'something is wrong'


if __name__ == '__main__':
    s = SpaceTraders()
    u = User()
    app = SpaceTradersApp()
    app.run()
