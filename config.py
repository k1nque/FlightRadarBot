import os
from logging.config import dictConfig
import logging
from asyncio import get_event_loop
from aiogram import Bot, Dispatcher, types

if os.path.isfile('secret.py'):
    from secret import token as TOKEN
else:
    TOKEN = os.getenv('TOKEN')

IsByWebhooks = False

if IsByWebhooks:
    WEBHOOK_HOST = "https://b8c3-45-9-46-141.eu.ngrok.io"
    WEBHOOK_PATH = ""
    WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
    WEBAPP_HOST = "127.0.0.1"
    WEBAPP_PORT = "8000"

bot = Bot(TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, loop=get_event_loop())

EPS = 2

# LOGGER_SETTINGS = {
#     "format": "%(asctime)s - %(name)s.%(funcName)s:%(lineno)d - %(levelname)s - %(message)s",  # noqa 501
#     "datefmt": "%Y-%m-%d %H:%M:%S",
#     "level": logging.DEBUG,
#     "handlers": [logging.StreamHandler()],
# }
#
# dictConfig(LOGGER_SETTINGS)
# logger = logging.getLogger(__name__)
