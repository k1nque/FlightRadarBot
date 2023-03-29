import sqlite3
import aiogram
from time import sleep
from models.user import User
from config import bot, TOKEN
import asyncio


async def startFlightDemon():
    while True:
        print('huj-8')
        users = getUsers()
        print(users)
        await processFlights(users)
        await asyncio.sleep(10)

def getUsers() -> sqlite3.Cursor:
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    users = cur.execute("""SELECT * from users WHERE user_state LIKE '%ready%'""")
    return users

async def processFlights(users: sqlite3.Cursor):
    print('huj-2')
    for user in users:
        print('huj-1')
        user = User(user)
        print('huj0')
        flights = user.getNearAircrafts()
        print(len(flights))
        if len(flights) == 0:
            await bot.send_message(user.UID, 'no aircrafts')
        for flight in flights:
            await bot.send_message(user.UID, f"*Flight ID*: {flight.id}\n"
                                       f"*Aircraft Code*: {flight.aircraft_code}\n"
                                       f"https://www.flightradar24.com/{flights[0].icao_24bit}/{flights[0].id}",
                             )


if __name__ == "__main__":
    asyncio.run(startFlightDemon())


