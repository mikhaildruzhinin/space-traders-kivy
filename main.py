import requests


class SpaceTraders(object):
    base_url = 'http://api.spacetraders.io'

    def __init__(self, username, token=None):
        self.username = username
        self.token = token

    def status(self):
        r = requests.get(f'{self.base_url}/game/status')
        r.raise_for_status()
        return r.json()

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
        body = {'type': 'STARTUP'}
        r = requests.post(f'{self.base_url}/users/{self.username}/loans', params=params, json=body)
        data = r.json()
        return data
