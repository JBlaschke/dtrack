import logging

from sys import argv

from ..auth import DBKey
from .      import make_default_connection

name = DBKey().host

#_______________________________________________________________________________
# Set up Logging
#

logger = logging.getLogger(name)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter(
    "[%(asctime)s - %(name)s - %(levelname)s] %(message)s"
)
ch.setFormatter(formatter)
logger.addHandler(ch)

logger = logging.getLogger("Connection Test")
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter(
    "[%(asctime)s - %(name)s - %(levelname)s] %(message)s"
)
ch.setFormatter(formatter)
logger.addHandler(ch)

#-------------------------------------------------------------------------------


#_______________________________________________________________________________
# Set up Connections
#

logger.info(f"Connecting to device: {name}")

logger.info("Connecting to database")
con = make_default_connection()

#-------------------------------------------------------------------------------

logger.info("Done -- SUCCESS!")