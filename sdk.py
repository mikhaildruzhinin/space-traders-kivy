import requests


class SpaceTraders(object):
    base_url = 'http://api.spacetraders.io'

    def __init__(self, username, token=None):
        self.username = username
        self.token = token

    def status(self):
        r = requests.get(f'{self.base_url}/game/status')
        r.raise_for_status()
        data = r.json()
        return data

    def generate_token(self):
        try:
            r = requests.post(f'{self.base_url}/users/{self.username}/token')
            data = r.json()
            r.raise_for_status()
            self.token = data['token']
        except requests.exceptions.HTTPError:
            pass
        return data

    def get_info(self):
        params = {'token': self.token}
        r = requests.get(f'{self.base_url}/users/{self.username}', params=params)
        data = r.json()
        return data

    def get_loans(self):
        params = {'token': self.token}
        r = requests.get(f'{self.base_url}/game/loans', params=params)
        data = r.json()
        return data
    
    def take_loan(self):
        params = {'token': self.token}
        payload = {'type': 'STARTUP'}
        r = requests.post(f'{self.base_url}/users/{self.username}/loans', params=params, json=payload)
        data = r.json()
        return data

    def get_ships(self, class_=None):
        params = {
            'token': self.token,
            'class': class_,
        }
        r = requests.get(f'{self.base_url}/game/ships', params=params)
        data = r.json()
        return data

    def buy_ship(self, location, type_):
        params = {'token': self.token}
        payload = {
            'location': location,
            'type': type_,
        }
        r = requests.post(f'{self.base_url}/users/{self.username}/ships', params=params, json=payload)
        data = r.json()
        return data

    def buy_goods(self, ship_id, good, quantity):
        params = {'token': self.token}
        payload = {
            'shipId': ship_id,
            'good': good,
            'quantity': quantity,
        }
        r = requests.post(f'{self.base_url}/users/{self.username}/purchase-orders', params=params, json=payload)
        data = r.json()
        return data

    def get_market(self, location):
        params = {'token': self.token}
        r = requests.get(f'{self.base_url}/game/locations/{location}/marketplace', params=params)
        data = r.json()
        return data

    def get_system_map(self, system, type_=None):
        params = {
            'token': self.token,
            'type': type_,
        }
        r = requests.get(f'{self.base_url}/game/systems/{system}/locations', params=params)
        data = r.json()
        return data

    def create_flight_plan(self, ship_id, destination):
        params = {'token': self.token}
        payload = {
            'shipId': ship_id,
            'destination': destination,
        }
        r = requests.post(f'{self.base_url}/users/{self.username}/flight-plans', params=params, json=payload)
        data = r.json()
        return data

    def get_flight_plan(self, flight_plan_id):
        params = {'token': self.token}
        r = requests.get(f'{self.base_url}/users/{self.username}/flight-plans/{flight_plan_id}', params=params)
        data = r.json()
        return data

    def sell_goods(self, ship_id, good, quantity):
        params = {'token': self.token}
        payload = {
            'shipId': ship_id,
            'good': good,
            'quantity': quantity,
        }
        r = requests.post(f'{self.base_url}/users/{self.username}/sell-orders', params=params, json=payload)
        data = r.json()
        return data

    def repay_loan(self, loan_id):
        params = {'token': self.token}
        r = requests.put(f'{self.base_url}/users/{self.username}/loans/{loan_id}', params=params)
        data = r.json()
        return data
