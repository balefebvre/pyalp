import os

from .api import Api



def get_path():
    '''TODO add doc...'''
    try:
        alp_path = os.environ['ALP_PATH']
        return alp_path
    except KeyError as error:
        # TODO enhance message...
        message = "Environment variable ALP_PATH not found!"
        raise Exception(message)
        exit()


def load_api(path):
    '''TODO add doc...'''
    try:
        api = Api(path)
    except OSError as error:
        # TODO enhance message...
        message = "ALP DLL '{}' not found!".format(path)
        print(message)
        exit()
