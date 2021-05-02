import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.clock import Clock
from kivy.network.urlrequest import UrlRequest
from space_traders import SpaceTraders
from pathlib import Path
import logging
import json
import certifi


kivy.require('2.0.0')
base_url = 'https://api.spacetraders.io'


class ConnectPage(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        url = f'{base_url}/game/status'
        self.server_status = UrlRequest(
            url=url,
            on_success=self.check_server_status,
            on_failure=self.check_server_status,
            method='GET',
            ca_file=certifi.where()
        )

    def check_server_status(self, *args):
        logging.info(f'[Game        ] {self.server_status.result["status"]}')
        self.status.text = self.server_status.result['status']

    def get_prev_user(self):
        if Path('user_details.txt').is_file():
            with open('user_details.txt', 'rt') as f:
                d = f.read().split(',')
            return d[0], d[1]
        return '', ''

    def submit_button(self, instance=None):
        self.error_message.text = ''
        if not self.username.text:
            self.error_message.text = 'Username is required.'
            logging.info(f'[Game        ] {self.error_message.text}')
            return None
        if not self.token.text:
            self.generate_token()
            return None
        if self.error_message.text:
            return None
        else:
            self.get_user_info()


    def generate_token(self):
        self.generated_token = UrlRequest(
            url=f'{base_url}/users/{self.username.text}/token',
            on_success=self.get_new_token,
            on_failure=self.show_generate_token_error_message,
            method='POST',
            ca_file=certifi.where()
        )

    def get_new_token(self, *args):
        self.token.text = self.generated_token.result['token']


    def show_generate_token_error_message(self, *args):
        self.error_message.text = self.generated_token.result['error']['message']
        logging.info(f'[Game        ] {self.generated_token.result["error"]["message"]}')

    def get_user_info(self, *args):
        self.user_info = UrlRequest(
            url=f'{base_url}/users/{self.username.text}',
            on_success=self.start_game,
            on_failure=self.show_user_info_error_message,
            req_headers={'Authorization': f'Bearer {self.token.text}'},
            method='GET',
            ca_file=certifi.where()
        )

    def show_user_info_error_message(self, *args):
        self.error_message.text = self.user_info.result['error']['message']
        logging.info(f'[Game        ] {self.user_info.result["error"]["message"]}')

    def start_game(self, *args):
        with open('user_details.txt', 'wt') as f:
            f.write(f'{self.username.text},{self.token.text}')
        app.username = self.username.text
        app.token = self.token.text
        app.user_info = self.user_info.result['user']
        Clock.schedule_once(self.log_in, 0.1)
        logging.info(f'[Game        ] {self.username.text} is logged in')

    def log_in(self, _):
        app.create_game_page()
        app.screen_manager.current = 'Game'


class Loans(BoxLayout):
    pass


class RV(RecycleView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        loans = s.get_loans()['response']['loans']
        self.data = [{'text': self.format_loan_text(loan)} for loan in loans]

    def format_loan_text(self, loan):
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
    def loans_button(self, instance=None):
        self.main_content.clear_widgets()
        self.loans = Loans()
        self.main_content.add_widget(self.loans)
        self.loans.user_loans_label.text = str(app.user_info['loans'])


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
