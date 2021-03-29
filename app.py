import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.clock import Clock
from space_traders import SpaceTraders
from pathlib import Path
import logging
import json


kivy.require('2.0.0')


class ConnectPage(BoxLayout):
    def check_server_status(self):
        server_status = SpaceTraders.get_status()
        if server_status['status_code'] == 200:
            return f'{server_status["response"]["status"]}'
        return 'something is wrong'

    def get_prev_user(self):
        if Path('user_details.txt').is_file():
            with open('user_details.txt', 'rt') as f:
                d = f.read().split(',')
            return d[0], d[1]
        return '', ''

    def submit_button(self, instance=None):
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
            self.error_message.text = user_info['response']['error']['message']
            logging.info(f'[Game        ] {user_info["response"]["error"]["message"]}')
            return None
        with open('user_details.txt', 'wt') as f:
            f.write(f'{s.username},{s.token}')
        Clock.schedule_once(self.log_in, 0.1)
        logging.info(f'[Game        ] {s.username} is logged in')

    def log_in(self, _):
        app.create_game_page()
        app.screen_manager.current = 'Game'


class Loans(BoxLayout):
    pass


class RV(RecycleView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        loans = s.get_loans()['response']['loans']
        self.data = [{'text': self.__format_loan_text(loan)} for loan in loans]

    def __format_loan_text(self, loan):
        bool_to_str = {
            True: 'yes',
            False: 'no',
        }
        text = f'\ntype: {loan["type"]}\n'
        text += f'amount: \u20B9 {loan["amount"]}\n'
        text += f'rate: {loan["rate"]} %\n'
        text += f'term: {loan["termInDays"]} days\n'
        text += f'required collateral: {bool_to_str[loan["collateralRequired"]]}\n'
        return text


class GamePage(BoxLayout):
    def get_username(self):
        return s.username

    def get_user_info(self):
        return s.get_user_info()['response']['user']

    def loans_button(self, instance=None):
        self.main_content.clear_widgets()
        self.loans = Loans()
        self.main_content.add_widget(self.loans)
        self.loans.user_loans_label.text = str(self.user_info['loans'])


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


if __name__ == '__main__':
    s = SpaceTraders()
    app = SpaceTradersApp()
    app.run()
