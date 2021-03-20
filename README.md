# space-traders-py

This is a Python wrapper for the [SpaceTraders API](https://spacetraders.io).

### How to install

Python3 should be already installed.
Install [`pipenv`](https://pipenv.pypa.io/en/latest/#install-pipenv-today) in order to manage a virtual environment.
Clone this repository and then use `pipenv` to install dependencies:
```
git clone https://github.com/mikhaildruzhinin/space-traders-py.git
pipenv install
```

### Getting Started

``` python
>>> from space_traders import SpaceTraders
>>> SpaceTraders.get_status()
{'response': {'status': 'spacetraders is currently online and available to play'}, 'status_code': 200}
>>> s = SpaceTraders('yourUsernameHere', 'yourTokenHere')
>>> s.get_user_info()
{'response': {'user': {'username': 'yourUsernameHere', 'credits': 0, 'ships': [], 'loans': []}}, 'status_code': 200}
```

### Licensing

This project is licensed under the [MIT License](https://github.com/mikhaildruzhinin/space-traders-py/blob/main/LICENSE).
