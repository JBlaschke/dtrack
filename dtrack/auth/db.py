from os          import environ
from dataclasses import dataclass

from .key import Key



@dataclass
class DBKey(Key):
    host:str
    name:str

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._host_key = kwargs.get("host_key", "DTRACK_HOST")
        self._name_key = kwargs.get("name_key", "DTRACK_NAME")

        self.host = environ[self._host_key]
        self.name = environ[self._name_key]