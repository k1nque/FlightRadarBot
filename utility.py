from sqlite3 import Connection
from json import loads


def getUserState(conn: Connection, UID: str) -> str:
    return loads(next(conn.execute("""SELECT user_state from users WHERE UID = ?""", (UID,)))[0])