from database import get_connection


def save_identity(wake_time, non_negotiables, ideal_self):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO identity_profile (wake_time, non_negotiables, ideal_self)
        VALUES (%s, %s, %s)
    """, (wake_time, non_negotiables, ideal_self))

    conn.commit()
    cur.close()
    conn.close()


def get_latest_identity():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT wake_time, non_negotiables, ideal_self
        FROM identity_profile
        ORDER BY created_at DESC
        LIMIT 1
    """)

    result = cur.fetchone()

    cur.close()
    conn.close()

    return result


def save_daily_log(log_text):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO daily_logs (log_text)
        VALUES (%s)
    """, (log_text,))

    conn.commit()
    cur.close()
    conn.close()


def get_latest_log():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT log_text
        FROM daily_logs
        ORDER BY created_at DESC
        LIMIT 1
    """)

    result = cur.fetchone()

    cur.close()
    conn.close()

    return result


def save_reinforcement(message):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO reinforcement_logs (message)
        VALUES (%s)
    """, (message,))

    conn.commit()
    cur.close()
    conn.close()