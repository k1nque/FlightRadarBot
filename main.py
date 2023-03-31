import sqlite3
import argparse
import threading
from bot import startBot
import asyncio
from flightDemon import startFlightDemon
from utility import dp, dbPath

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    args = parser.parse_args()

    conn = sqlite3.connect(dbPath)
    cur = conn.cursor()
    with open('SQL_scripts/database_init.sql', 'r') as file:
        script = file.read()
        cur.execute(script)

    dp.loop.create_task(startFlightDemon())
    startBot()
