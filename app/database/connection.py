import pymysql
from pymysql.cursors import DictCursor
from flask import g
from app.config import DATABASE_CONFIG


class DatabaseManager:

    @staticmethod
    def init_app(app):
        @app.teardown_appcontext
        def close(exception=None):
            conns = g.pop('_db_connections', {})
            for db_name, conn in conns.items():
                try:
                    if exception:
                        conn.rollback()
                    conn.close()
                except Exception:
                    pass

    @staticmethod
    def get_connection(db_name='estadio_db'):
        if '_db_connections' not in g:
            g._db_connections = {}
        if db_name not in g._db_connections:
            cfg = DATABASE_CONFIG[db_name].copy()
            cfg['cursorclass'] = DictCursor
            g._db_connections[db_name] = pymysql.connect(**cfg)
            g._db_connections[db_name].autocommit(False)
        return g._db_connections[db_name]
