import os
from logging.config import dictConfig
import logging


if os.path.isfile('secret.py'):
    from secret import token as TOKEN
else:
    TOKEN = os.getenv('TOKEN')

IsByWebhooks = True
IsInDocker = False

if IsByWebhooks:
    WEBHOOK_HOST = "https://2417-45-9-46-141.eu.ngrok.io"
    WEBHOOK_PATH = ""
    WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
    WEBAPP_HOST = "127.0.0.1"
    WEBAPP_PORT = "8000"



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
