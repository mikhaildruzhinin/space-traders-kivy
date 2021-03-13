import requests


class SpaceTraders(object):
    base_url = 'http://api.spacetraders.io'

    def __init__(self, username, token):
        pass

    def status(self):
        r = requests.get(f'{self.base_url}/game/status')
        r.raise_for_status()
        return r.json()

    def generate_token(self, username):
        try:
            r = requests.post(f'{self.base_url}/users/{username}/token')
            data = r.json()
            r.raise_for_status()
            self.token = data['token']
            self.username = data['user']['username']
        except requests.exceptions.HTTPError:
            pass
        return data

    def get_info(self, username, token):
        params = {'token': token}
        r = requests.get(f'{self.base_url}/users/{username}', params=params)
        data = r.json()
        r.raise_for_status()
        return data
