import os

from . import Api


def get_path():
    """TODO add docstring."""
    try:
        alp_path = os.environ['ALP_PATH']
        return alp_path
    except KeyError:
        message = "Environment variable ALP_PATH not found!"
        raise Exception(message)


def load_api(path):
    """TODO add docstring."""
    try:
        api = Api(path)
        return api
    except OSError:
        message = "ALP DLL '{}' not found!".format(path)
        raise Exception(message)


# Retrieve Vialux ALP path
path = get_path()

# Load Vialux ALP API
api = load_api(path)
