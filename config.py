import os
from logging.config import dictConfig
import logging
from asyncio import get_event_loop
from aiogram import Bot, Dispatcher

if os.path.isfile('secret.py'):
    from secret import token as TOKEN
else:
    TOKEN = os.getenv('TOKEN')

IsByWebhooks = False



if IsByWebhooks:
    WEBHOOK_HOST = ""
    WEBHOOK_PATH = ""
    WEBHOOK_URL = ""
    WEBAPP_HOST = ""
    WEBAPP_PORT = ""
    bot = None
    # TODO Webhooks
else:
    bot = Bot(TOKEN)
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
