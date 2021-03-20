import requests


class SpaceTraders(object):
    '''SpaceTraders API wrapper'''
    base_url = 'https://api.spacetraders.io'

    def __init__(self, username, token=None):
        '''Constructor'''
        self.username = username
        self.token = token

    # flight plans
    def get_flight_plans(self, system='OE'):
        '''Get all active flightPlans in the system'''
        params = {'token': self.token}
        url = f'{self.base_url}/game/systems/{system}/flight-plans'
        r = requests.get(f'{self.base_url}/game/systems/{system}/flight-plans', params=params)
        data = {'response': r.json(), 'status_code': r.status_code}
        return data

    def get_flight_plan(self, flight_plan_id):
        '''Get info on an existing flight plan'''
        params = {'token': self.token}
        r = requests.get(f'{self.base_url}/users/{self.username}/flight-plans/{flight_plan_id}', params=params)
        data = {'response': r.json(), 'status_code': r.status_code}
        return data

    def submit_flight_plan(self, ship_id, destination):
        '''Submit a new flight plan'''
        params = {'token': self.token}
        payload = {
            'shipId': ship_id,
            'destination': destination,
        }
        r = requests.post(f'{self.base_url}/users/{self.username}/flight-plans', params=params, json=payload)
        data = {'response': r.json(), 'status_code': r.status_code}
        return data

    # game
    @classmethod
    def get_status(cls):
        '''Use to determine whether the server is alive'''
        r = requests.get(f'{cls.base_url}/game/status')
        data = {'response': r.json(), 'status_code': r.status_code}
        return data

    # loans
    def get_loans(self):
        '''Get available loans'''
        params = {'token': self.token}
        r = requests.get(f'{self.base_url}/game/loans', params=params)
        data = {'response': r.json(), 'status_code': r.status_code}
        return data

    def get_user_loans(self):
        '''Get your loans'''
        params = {'token': self.token}
        r = requests.get(f'{self.base_url}/users/{self.username}/loans', params=params)
        data = {'response': r.json(), 'status_code': r.status_code}
        return data

    def repay_loan(self, loan_id):
        '''Pay off a loan'''
        params = {'token': self.token}
        r = requests.put(f'{self.base_url}/users/{self.username}/loans/{loan_id}', params=params)
        data = {'response': r.json(), 'status_code': r.status_code}
        return data

    def take_loan(self, type_):
        '''Request a new loan'''
        params = {'token': self.token}
        payload = {'type': type_}
        r = requests.post(f'{self.base_url}/users/{self.username}/loans', params=params, json=payload)
        data = {'response': r.json(), 'status_code': r.status_code}
        return data

    # locations
    def get_docked_ships(self, location):
        '''Get info on a location's docked ships'''
        params = {'token': self.token}
        r = requests.get(f'{self.base_url}/game/locations/{location}/ships', params=params)
        data = {'response': r.json(), 'status_code': r.status_code}
        return data

    def get_location_info(self, location):
        '''Get info on a location'''
        params = {'token': self.token}
        r = requests.get(f'{self.base_url}/game/locations/{location}', params=params)
        data = {'response': r.json(), 'status_code': r.status_code}
        return data

    def get_system_locations(self, system='OE', type_=None):
        '''Get locations in a system'''
        params = {
            'token': self.token,
            'type': type_,
        }
        r = requests.get(f'{self.base_url}/game/systems/{system}/locations', params=params)
        data = {'response': r.json(), 'status_code': r.status_code}
        return data

    # marketplace
    def get_market(self, location):
        '''Get info on a locations marketplace'''
        params = {'token': self.token}
        r = requests.get(f'{self.base_url}/game/locations/{location}/marketplace', params=params)
        data = {'response': r.json(), 'status_code': r.status_code}
        return data

    # purchase orders
    def buy_goods(self, ship_id, good, quantity):
        '''Place a new purchase order'''
        params = {'token': self.token}
        payload = {
            'shipId': ship_id,
            'good': good,
            'quantity': quantity,
        }
        r = requests.post(f'{self.base_url}/users/{self.username}/purchase-orders', params=params, json=payload)
        data = {'response': r.json(), 'status_code': r.status_code}
        return data

    # sell orders
    def sell_goods(self, ship_id, good, quantity):
        '''Place a new sell order'''
        params = {'token': self.token}
        payload = {
            'shipId': ship_id,
            'good': good,
            'quantity': quantity,
        }
        r = requests.post(f'{self.base_url}/users/{self.username}/sell-orders', params=params, json=payload)
        data = {'response': r.json(), 'status_code': r.status_code}
        return data

    # ships
    def buy_ship(self, location, type_):
        '''Buy a new ship'''
        params = {'token': self.token}
        payload = {
            'location': location,
            'type': type_,
        }
        r = requests.post(f'{self.base_url}/users/{self.username}/ships', params=params, json=payload)
        data = {'response': r.json(), 'status_code': r.status_code}
        return data

    def get_ships(self, class_=None):
        '''Get info on available ships'''
        params = {
            'token': self.token,
            'class': class_,
        }
        r = requests.get(f'{self.base_url}/game/ships', params=params)
        data = {'response': r.json(), 'status_code': r.status_code}
        return data

    def get_ship_info(self, ship_id):
        '''Get your ship info'''
        params = {'token': self.token}
        r = requests.get(f'{self.base_url}/users/{self.username}/ships/{ship_id}', params=params)
        data = {'response': r.json(), 'status_code': r.status_code}
        return data

    def get_user_ships(self):
        '''Get your ships'''
        params = {'token': self.token}
        r = requests.get(f'{self.base_url}/users/{self.username}/ships', params=params)
        data = {'response': r.json(), 'status_code': r.status_code}
        return data

    def jettison_cargo(self, ship_id, good, quantity):
        '''Jettison cargo'''
        params = {
            'token': self.token,
            'good': good,
            'quantity': quantity,
        }
        r = requests.put(f'{self.base_url}/users/{self.username}/ships/{ship_id}/jettison', params=params)
        data = {'response': r.json(), 'status_code': r.status_code}
        return data

    def sell_ship(self, ship_id):
        '''Scrap your ship for credits'''
        params = {'token': self.token}
        r = requests.delete(f'{self.base_url}/users/{self.username}/ships/{ship_id}', params=params)
        data = {'response': r.json(), 'status_code': r.status_code}
        return data

    # systems
    def get_systems_info(self):
        '''Get systems info'''
        params = {'token': self.token}
        r = requests.get(f'{self.base_url}/game/systems', params=params)
        data = {'response': r.json(), 'status_code': r.status_code}
        return data

    # users
    def generate_token(self):
        '''Claim a username and get a token'''
        try:
            r = requests.post(f'{self.base_url}/users/{self.username}/token')
            data = {'response': r.json(), 'status_code': r.status_code}
            r.raise_for_status()
            self.token = data['response']['token']
        except requests.exceptions.HTTPError:
            pass
        return data

    def get_user_info(self):
        '''Get your info'''
        params = {'token': self.token}
        r = requests.get(f'{self.base_url}/users/{self.username}', params=params)
        data = {'response': r.json(), 'status_code': r.status_code}
        return data
