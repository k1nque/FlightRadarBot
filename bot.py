from aiogram import Dispatcher, Bot, executor, types
from aiogram.dispatcher.filters import CommandStart, CommandHelp, Command
from config import TOKEN, dp, IsByWebhooks
import config
from json import dumps
import sqlite3
from utility import getUserState
import re

conn = sqlite3.connect('/db/users.db')

"""
UserState is a dict object with keys:
    1) NO-LOCATION -- Location in DB is null, READY cannot be True
    2) NO-DISTANCE -- Distance in DB is null, READY cannot be True
    3) CHANGE-LOCATION -- Old location is in DB, but READY can be True
    4) CHANGE-DISTANCE -- Old distance is in DB, but READY can be True
    5) READY -- flightDemon will send notifications to that user
"""


def startBot():
    if IsByWebhooks:
        executor.start_webhook(dispatcher=dp,
                               webhook_path=config.WEBHOOK_PATH,
                               on_startup=None,
                               on_shutdown=None,
                               skip_updates=True,
                               host=config.WEBAPP_HOST,
                               port=config.WEBAPP_PORT)
    else:
        executor.start_polling(dp, skip_updates=True)


@dp.message_handler(CommandStart())
async def start(msg: types.Message):
    conn.execute("""INSERT OR REPLACE INTO users(UID, user_state) VALUES(?, ?)""",
                   (msg.chat.id, dumps({"NO-LOCATION": True,
                                        "NO-DISTANCE": True,
                                        "CHANGE-LOCATION": False,
                                        "CHANGE-DISTANCE": False,
                                        "READY": False})))
    conn.commit()
    await msg.answer("Hello, I'm <b><i>Flight Radar Bot</i></b>, send me your location,"
                     " and I will send you notifications about aircrafts flying near you")


@dp.message_handler(content_types=types.ContentType.LOCATION)
async def location(msg: types.Message):
    userState = getUserState(conn, msg.chat.id)
    userState["NO-LOCATION"] = False
    conn.execute("""
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
        await msg.answer("Send me distance-threshold to aircraft in km")
    else:
        await msg.answer("Your new location is <b>saved</b>")


@dp.message_handler(CommandHelp())
async def help(msg: types.Message):
    pass  # TODO Do Help


@dp.message_handler(Command('set_location'))
async def set_location(msg: types.Message):
    userState = getUserState(conn, msg.chat.id)
    userState["CHANGE-LOCATION"] = True
    userState["CHANGE-DISTANCE"] = False
    conn.execute("""UPDATE users SET user_state = ?""", (dumps(userState),))
    conn.commit()
    await msg.answer("Now you can send me <b>location</b>!")


@dp.message_handler(Command('set_distance'))
async def set_distance(msg: types.Message):
    userState = getUserState(conn, msg.chat.id)
    userState["CHANGE-DISTANCE"] = True
    userState["CHANGE-LOCATION"] = False
    conn.execute("""UPDATE users SET user_state = ?""", (dumps(userState),))
    conn.commit()
    await msg.answer("Now you can send me distance threshold in <b><i>metres</i><b>")


@dp.message_handler()
async def any(msg: types.Message):
    userState = getUserState(conn, msg.chat.id)
    if not userState["CHANGE-LOCATION"] and (userState["CHANGE-DISTANCE"] or userState["NO-DISTANCE"]):
        try:
            dist = int(msg.text)
            userState["CHANGE-DISTANCE"] = False
            userState["NO-DISTANCE"] = False
            if not userState["NO-LOCATION"]:
                userState["READY"] = True
            conn.execute("""UPDATE users SET user_state = ?, distance = ? WHERE UID = ?""",
                           (dumps(userState), dist, msg.chat.id))
            await msg.answer("New distance threshold is saved")
            conn.commit()
        except ValueError:
            await msg.answer("Distance is incorrect")

    elif userState["CHANGE-LOCATION"]:
        try:
            print(msg.text)
            coords = re.findall('(\-?\d+\.?\d*)', msg.text)

            if len(coords) != 2:
                await msg.answer("Location coordinates is incorrect")
            else:
                lat, lon = coords
                await msg.answer("Your new location is <b>saved</b>")
                conn.execute("""UPDATE users SET latitude = ?, longitude = ? WHERE UID = ?""", (lat, lon, msg.chat.id))
        except:
            await msg.answer("Location coordinates is incorrect")


if __name__ == "__main__":
    bot = Bot(TOKEN)
    dp = Dispatcher(bot)
