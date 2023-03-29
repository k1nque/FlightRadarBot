from aiogram import Dispatcher, Bot, executor, types
from aiogram.dispatcher.filters import CommandStart, CommandHelp, Command
from config import TOKEN, bot, dp, IsByWebhooks
import sqlite3
from utility import getUserState

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

def startBot():
    executor.start_polling(dp, skip_updates=True)


@dp.message_handler(CommandStart())
async def start(msg: types.Message):  # TODO Change UserState
    cursor.execute("""INSERT OR REPLACE INTO users(UID, user_state) VALUES(?, ?)""",
                   (msg.chat.id, "no-loc no-dist"))
    conn.commit()
    await msg.answer("Hello, I'm Flight Radar Bot, send me your location,"
                     " and I will send you notifications about aircrafts flying near you")

@dp.message_handler(content_types=types.ContentType.LOCATION)
async def location(msg: types.Message):
    userState = getUserState(conn, msg.chat.id)
    if 'change-loc' not in userState:
        await msg.answer("Enter the command /set_location, if you want to change your location")
    else:
        cursor.execute("""
            UPDATE users SET 
                latitude = ?,
                longitude = ?,
                user_state = ?
            WHERE UID = ?
            """, (
            msg.location.latitude,
            msg.location.longitude,
            userState.replace('change-loc', ''),
            msg.chat.id))
    conn.commit()
    if 'no-dist' in userState:
        await msg.answer("Now send me distance-threshold to aircraft in meters")
    else:
        await msg.answer("Your new location is *saved*", parse_mode='MarkdownV2')

@dp.message_handler(CommandHelp())
async def help(msg: types.Message):
    pass  # TODO Do Help

@dp.message_handler(Command('set_location'))  # TODO Change UserState
async def set_location(msg: types.Message):
    userState = getUserState(conn, msg.chat.id)
    conn.execute("""UPDATE users SET user_state = ?""", (userState + ' change-loc',))
    conn.commit()
    await msg.answer("Now you can send me location!")


@dp.message_handler(Command('set_distance'))
async def set_distance(msg: types.Message):
    userState = getUserState(conn, msg.chat.id)
    if 'no-dist' in userState:
        conn.execute("""UPDATE users SET user_state = ?""", (userState.replace('no-dist', 'change-dist')))

    else:
        conn.execute("""UPDATE users SET user_state = ?""", (userState+' change-dist',))
    conn.commit()
    await msg.answer("Now you can send me distance threshold in metres")

@dp.message_handler()
async def any(msg: types.Message):
    try:
        dist = int(msg.text)
        userState = getUserState(conn, msg.chat.id)
        if 'no-dist' in userState or 'change-dist' in userState:
            cursor.execute("""UPDATE users SET user_state = ?, distance = ? WHERE UID = ?""",
                           ('ready' if userState.replace('no-dist', '').replace('change-dist', '')
                                       == '' else userState.replace('no-dist', '').replace('change-dist', ''),
                            dist, msg.chat.id))
            await msg.answer("New distance threshold is saved")
        conn.commit()
    except ValueError as er:
        print(er)  # TODO Process ValueError


if __name__ == "__main__":
    bot = Bot(TOKEN)
    dp = Dispatcher(bot)

