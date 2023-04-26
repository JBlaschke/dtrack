from .connection  import Connection
from .transaction import DBTransactionAdapter
from ..auth       import DBKey



def make_default_connection():
    key = DBKey()
    return Connection(key)