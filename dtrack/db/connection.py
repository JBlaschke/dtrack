import logging

from MySQLdb  import connect, OperationalError
from textwrap import dedent


class Connection(object):

    def __init__(self, db_key):
        self._db_key = db_key
        self._name   = db_key.name
        self._table  = "dtrack"
        self._logger = logging.getLogger(db_key.host)
        self._connect()


    def _connect(self):
        self._db = connect(
                host = self._db_key.host,
                user = self._db_key.username,
                passwd = self._db_key.password
            )

        self._logger.info("User: {} extablished connection to: {}".format(
            self._db_key.username, self._db_key.host
        ))

        self._cursor = self._db.cursor()
        self._ensure_db()
        self._cursor.execute(f"USE {self.name}")
        self._ensure_table()

        self._logger.info(f"Connection using DATABASE: {self.name}")


    def __del__(self):
        try:
            self.cursor.close()
            self.db.close()
        except (AttributeError, OperationalError):
            self._logger.warning("Connection failed, ignoring!")
            pass


    def execute(self, str_query):
        try:
            r = self.cursor.execute(str_query)
        except (AttributeError, OperationalError):
            self._logger.warning("Connection failed, retrying!")
            try:
                self._connect()
            except (AttributeError, OperationalError):
                self._logger.error("Failed to reconnect on error!")
                return 0
            r = self.cursor.execute(str_query)
        return r


    def commit(self):
        try:
            r = self._db.commit()
        except (AttributeError, OperationalError):
            self._logger.warning("Connection failed, retrying!")
            try:
                self._connect()
            except (AttributeError, OperationalError):
                self._logger.error("Failed to reconnect on error!")
                return 0
            r = self._db.commit()
        return r


    @property
    def result(self):
        return self.cursor.fetchone()


    @property
    def results(self):
        return self.cursor.fetchall()


    def _ensure_db(self):
        r = self.execute(f"SHOW DATABASES LIKE '{self.name}'")
        if r == 0:
            self._create_db()


    def _create_db(self):
        self.execute(f"CREATE DATABASE {self.name}")


    def _show_table(self, name):
        return self.execute(f"SHOW TABLES LIKE '{name}'")


    def _ensure_table(self):
        r = self._show_table(self.table)
        if r == 0:
            self._create_main_table()


    def _create_main_table(self):
        sql_cmd = dedent(
            f"""\
            CREATE TABLE {self.table} (
                idx INT UNSIGNED NOT NULL AUTO_INCREMENT,
                t DOUBLE, fingerprint VARCHAR(16),
                rank INT UNSIGNED,
                slurm_job_id VARCHAR(64),
                slurm_node_list VARCHAR(1024),
                function_name VARCHAR(64),
                file_path VARCHAR(1024),
                file_offset INT UNSIGNED,
                PRIMARY KEY(idx)
            )
            """
        ).rstrip()
        self.execute(sql_cmd)
        self.commit()


    @property
    def cursor(self):
        return self._cursor


    @property
    def db(self):
        return self._db


    @property
    def name(self):
        return self._name


    @property
    def table(self):
        return self._table