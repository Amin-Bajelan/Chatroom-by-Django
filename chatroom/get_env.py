from os import environ
from dotenv import load_dotenv
load_dotenv()

# GET ENV VARIABLE 
def get_my_env(key, default=None, optinal=False):
    """Return environment variables with some options."""
    val = environ.get(key)
    if val is not None:
        return val
    elif default is not None:
        return default
    elif not optinal:
        raise ValueError(f"Environment variable {key} was not defined")
