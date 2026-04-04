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

def insert_bot_entry(bot_code: str, telegram_user_id: int):
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("""
                insert into bot_events (
                    event_time,
                    event_date,
                    bot_id,
                    telegram_user_id,
                    event_type,
                    status
                )
                values (
                    now(),
                    current_date,
                    (
                        select id from bots where code = %s
                    ),
                    %s,
                    'bot_entry',
                    'success'
                )
            """, (bot_code, telegram_user_id))
        conn.commit()
    finally:
        if conn:
            conn.close()