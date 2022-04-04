from os          import environ
from dataclasses import dataclass



@dataclass
class Key:
    username:str
    password:str

    def __init__(self, *args, **kwargs):
        self._username_key = kwargs.get("username_key", "DTRACK_USER")
        self._password_key = kwargs.get("password_key", "DTRACK_PASSWORD")

        self.username = environ[self._username_key]
        self.password = environ[self._password_key]