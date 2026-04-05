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

def insert_bot_event(
    bot_code: str,
    telegram_user_id: int,
    event_type: str,
    status: str = "success",
    mode: str | None = None,
    error_text_short: str | None = None,
    file_size_bytes: int | None = None
):
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
                    status,
                    mode,
                    error_text_short,
                    file_size_bytes
                )
                values (
                    now(),
                    current_date,
                    (
                        select id from bots where code = %s
                    ),
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
            """, (
                bot_code,
                telegram_user_id,
                event_type,
                status,
                mode,
                error_text_short,
                file_size_bytes
            ))
        conn.commit()
    finally:
        if conn:
            conn.close()