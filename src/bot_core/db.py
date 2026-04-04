import os
import psycopg2


def get_database_url() -> str:
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise RuntimeError("DATABASE_URL is not set")
    return db_url


def get_connection():
    return psycopg2.connect(get_database_url())


def test_connection() -> bool:
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("select 1")
            cur.fetchone()
        return True
    finally:
        if conn:
            conn.close()