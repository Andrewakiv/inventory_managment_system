from contextlib import contextmanager
import psycopg2
from .db_config import DB_CONFIG


@contextmanager
def get_db_cursor():
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        yield conn.cursor()
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
