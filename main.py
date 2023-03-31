import sqlite3
import argparse
import threading
from bot import startBot
import asyncio
from flightDemon import startFlightDemon
from config import dp


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--create-db', action='store_true')


    args = parser.parse_args()

    if args.create_db:
        conn = sqlite3.connect('/db/users.db')
        cur = conn.cursor()
        with open('SQL_scripts/database_init.sql', 'r') as file:
            script = file.read()
            cur.execute(script)

    else:
        dp.loop.create_task(startFlightDemon())
        startBot()