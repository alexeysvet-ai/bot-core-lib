from bot_core.db import get_connection


def get_user_lang(bot_code: str, telegram_user_id: int):
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("""
                select us.lang_code
                from user_settings us
                join bots b on b.id = us.bot_id
                where b.code = %s
                  and us.telegram_user_id = %s
                limit 1
            """, (bot_code, telegram_user_id))
            row = cur.fetchone()
            return row[0] if row else None
    finally:
        if conn:
            conn.close()


def set_user_lang(bot_code: str, telegram_user_id: int, lang_code: str):
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("""
                insert into user_settings (
                    telegram_user_id,
                    bot_id,
                    lang_code,
                    created_at,
                    updated_at
                )
                values (
                    %s,
                    (
                        select id from bots where code = %s
                    ),
                    %s,
                    now(),
                    now()
                )
                on conflict (telegram_user_id, bot_id)
                do update set
                    lang_code = excluded.lang_code,
                    updated_at = now()
            """, (telegram_user_id, bot_code, lang_code))
        conn.commit()
    finally:
        if conn:
            conn.close()