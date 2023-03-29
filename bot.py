from aiogram import Dispatcher, Bot, executor, types
from aiogram.dispatcher.filters import CommandStart, CommandHelp, Command
from config import TOKEN, bot, dp, IsByWebhooks
from json import dumps
import sqlite3
from utility import getUserState

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

"""
UserState is a dict object with keys:
    1) NO-LOCATION -- Location in DB is null, READY cannot be True
    2) NO-DISTANCE -- Distance in DB is null, READY cannot be True
    3) CHANGE-LOCATION -- Old location is in DB, but READY can be True
    4) CHANGE-DISTANCE -- Old distance is in DB, but READY can be True
    5) READY -- flightDemon will send notifications to that user
"""


def startBot():
    executor.start_polling(dp, skip_updates=True)


@dp.message_handler(CommandStart())
async def start(msg: types.Message):
    cursor.execute("""INSERT OR REPLACE INTO users(UID, user_state) VALUES(?, ?)""",
                   (msg.chat.id, dumps({"NO-LOCATION": True,
                                        "NO-DISTANCE": True,
                                        "CHANGE-LOCATION": False,
                                        "CHANGE-DISTANCE": False,
                                        "READY": False})))
    conn.commit()
    await msg.answer("Hello, I'm Flight Radar Bot, send me your location,"
                     " and I will send you notifications about aircrafts flying near you")


@dp.message_handler(content_types=types.ContentType.LOCATION)
async def location(msg: types.Message):
    userState = getUserState(conn, msg.chat.id)
    userState["NO-LOCATION"] = False
    cursor.execute("""
            UPDATE users SET 
                latitude = ?,
                longitude = ?,
                user_state = ?
            WHERE UID = ?
            """, (
        msg.location.latitude,
        msg.location.longitude,
        dumps(userState),
        msg.chat.id))
    conn.commit()
    if userState["NO-DISTANCE"]:
        await msg.answer("Now send me distance-threshold to aircraft in meters")
    else:
        await msg.answer("Your new location is *saved*", parse_mode='MarkdownV2')


@dp.message_handler(CommandHelp())
async def help(msg: types.Message):
    pass  # TODO Do Help


@dp.message_handler(Command('set_location'))
async def set_location(msg: types.Message):
    userState = getUserState(conn, msg.chat.id)
    userState["CHANGE-LOCATION"] = True
    conn.execute("""UPDATE users SET user_state = ?""", (dumps(userState),))
    conn.commit()
    await msg.answer("Now you can send me location!")


@dp.message_handler(Command('set_distance'))
async def set_distance(msg: types.Message):
    userState = getUserState(conn, msg.chat.id)
    userState["CHANGE-DISTANCE"] = True
    conn.execute("""UPDATE users SET user_state = ?""", (dumps(userState),))
    conn.commit()
    await msg.answer("Now you can send me distance threshold in metres")


@dp.message_handler()
async def any(msg: types.Message):
    userState = getUserState(conn, msg.chat.id)
    if userState["CHANGE-DISTANCE"] or userState["NO-DISTANCE"]:
        try:
            dist = int(msg.text)
            userState["CHANGE-DISTANCE"] = False
            userState["NO-DISTANCE"] = False
            if not userState["NO-LOCATION"]:
                userState["READY"] = True
            cursor.execute("""UPDATE users SET user_state = ?, distance = ? WHERE UID = ?""",
                           (dumps(userState), dist, msg.chat.id))
            await msg.answer("New distance threshold is saved")
            conn.commit()
        except ValueError:
            await msg.answer("Distance is incorrect")
    elif userState["CHANGE-LOCATION"]: #TODO Change location by coords
        try:
            pass
        except:
            pass


if __name__ == "__main__":
    bot = Bot(TOKEN)
    dp = Dispatcher(bot)
