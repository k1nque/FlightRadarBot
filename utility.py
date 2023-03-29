from sqlite3 import Connection


def getUserState(conn: Connection, UID: str) -> str:
    return next(conn.execute("""SELECT user_state from users WHERE UID = ?""", (UID,)))[0]