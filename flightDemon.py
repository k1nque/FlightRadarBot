import sqlite3
from models.user import User
from config import bot
import asyncio


async def startFlightDemon():
    conn = sqlite3.connect('/db/users.db')
    while True:
        users = getUsers(conn)
        await processFlights(users, conn)
        await asyncio.sleep(10)

def getUsers(conn) -> sqlite3.Cursor:
    users = conn.execute("""SELECT * from users""")
    return users

async def processFlights(users: sqlite3.Cursor, conn: sqlite3.Connection):
    for user in users:
        user = User(user)
        if not user.isReady:
            continue
        flights = user.getNearAircrafts()
        # if len(flights) == 0:
        #     await bot.send_message(user.UID, 'no aircrafts')
        for flight in flights:
            await bot.send_message(user.UID, f"<b>Flight I</b>: {flight.id}\n"
                                       f"<b>Aircraft Code</b>: {flight.aircraft_code}\n"
                                       f"https://www.flightradar24.com/{flight.icao_24bit}/{flight.id}",
                             )
        conn.execute("""UPDATE users SET notified = ? WHERE UID = ?""", (user.notified, user.UID))
        conn.commit()


if __name__ == "__main__":
    asyncio.run(startFlightDemon())


