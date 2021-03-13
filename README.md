# space-traders-py

This is a Python wrapper for the [SpaceTraders API](https://spacetraders.io).

### How to install

Python3 should be already installed.
Install `[pipenv](https://pipenv.pypa.io/en/latest/#install-pipenv-today)` in order to manage a virtual environment.
Clone this repository and then use `pipenv` to install dependencies:
```
git clone https://github.com/mikhaildruzhinin/space-traders-py.git
pipenv install
```

### Getting Started

``` python
>>> from sdk import SpaceTraders
>>> s = SpaceTraders('yourUsernameHere', 'yourTokenHere')
>>> s.status()
{'status': 'spacetraders is currently online and available to play'}
>>> s.get_info()
{'user': {'username': 'test-py-client', 'credits': 0, 'ships': [], 'loans': []}}
```

### Licensing

This project is licensed under the [MIT License](https://github.com/mikhaildruzhinin/space-traders-py/blob/main/LICENSE).
