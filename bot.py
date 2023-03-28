from aiogram import Dispatcher, Bot, executor, types
from aiogram.dispatcher.filters import CommandStart, CommandHelp, Command
from config import TOKEN
import sqlite3

bot = Bot(TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(CommandStart())
async def start(msg: types.Message):  # TODO Change UserState
    cursor.execute("""INSERT INTO users(UID, user_state) VALUES(?, ?)""",
                   (msg.chat.id, "no-loc no-dist"))
    conn.commit()
    await msg.answer("Hello, I'm Flight Radar Bot, send me your location,"
                     " and I will send you notifications about aircrafts flying near you")


@dp.message_handler(content_types=types.ContentType.LOCATION)
async def location(msg: types.Message):
    cursor.execute("""
        UPDATE users SET 
            latitude = ?,
            longitude = ?,
            user_state = ?
        WHERE UID = ?
        """, (
        msg.location.latitude,
        msg.location.longitude,
        'no-dist',
        msg.chat.id
    )
                   )
    conn.commit()
    await msg.answer("Now send me distance-threshold to aircraft in meters")


@dp.message_handler(CommandHelp())
async def help(msg: types.Message):
    pass  # TODO Do Help


@dp.message_handler(Command('set_location'))  # TODO Change UserState
async def set_location(msg: types.Message):
    await msg.answer("Now you can send me location!")


@dp.message_handler()
async def any(msg: types.Message):
    try:
        dist = int(msg.text)
        user_state = cursor.execute("""SELECT user_state FROM users WHERE UID = ?""", msg.chat.id)
        # TODO Fix Select
        if user_state == 'no-dist':
            cursor.execute("""UPDATE users SET user_state = ?, distance = ? WHERE UID = ?""",
                           ('ready', dist, msg.chat.id))
        conn.commit()
    except ValueError:
        pass # TODO Process ValueError

if __name__ == "__main__":
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    executor.start_polling(dp, skip_updates=True)
