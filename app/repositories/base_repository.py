from app.database.connection import DatabaseManager


class BaseRepository:
    def __init__(self, db_name='estadio_db'):
        self.db_name = db_name

    @property
    def _conn(self):
        return DatabaseManager.get_connection(self.db_name)

    def fetch_all(self, sql, params=None):
        with self._conn.cursor() as cur:
            cur.execute(sql, params or ())
            return cur.fetchall()

    def fetch_one(self, sql, params=None):
        with self._conn.cursor() as cur:
            cur.execute(sql, params or ())
            return cur.fetchone()

    def execute(self, sql, params=None):
        conn = self._conn
        with conn.cursor() as cur:
            cur.execute(sql, params or ())
            conn.commit()
            return cur.lastrowid

    def execute_many(self, sql, params_list):
        conn = self._conn
        with conn.cursor() as cur:
            cur.executemany(sql, params_list)
            conn.commit()

    def commit(self):
        self._conn.commit()

    def rollback(self):
        self._conn.rollback()
