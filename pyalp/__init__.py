from .base import get_path, load_api



# Retrieve Vialux ALP path
path = get_path()

# Load Vialux ALP API
api = load_api(path)




from . import device, sequence, protocol



__all__ = [
    'path',
    'api',
    'device',
    'sequence',
    'protocol',
]
