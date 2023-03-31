from sqlite3 import Connection
from json import loads
from config import IsByWebhooks, IsInDocker, TOKEN, WEBHOOK_URL
from asyncio import get_event_loop
from aiogram import Bot, Dispatcher, types

bot = Bot(TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, loop=get_event_loop())

if IsInDocker:
    dbPath = "/db/users.db"
else:
    dbPath = "users.db"

async def onStartup(dp: Dispatcher):
    await dp.bot.set_webhook(WEBHOOK_URL)

async def onShutdown(dp: Dispatcher):
    await bot.delete_webhook()



def getUserState(conn: Connection, UID: str) -> str:
    return loads(next(conn.execute("""SELECT user_state from users WHERE UID = ?""", (UID,)))[0])