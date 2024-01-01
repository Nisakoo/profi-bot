import os
import asyncio

import logging_config
import logging

from dotenv import load_dotenv

from bot.telegram.bot import TelegramBot
from neural_network.gigachat.gigachat import GigaChatNeuralNetwork
from db.sqlite3_db.sqlite3_db import Sqlite3DataBase

from tests.gigachat_test.gigachat_test import GigaChatTest
from tests.review.review import Review


if __name__ == "__main__":
    load_dotenv()

    db = Sqlite3DataBase(filename=os.environ["DATABASE_FILE"])
    loop = asyncio.get_event_loop()
    loop.run_until_complete(db.connect())

    try:
        TelegramBot(
            os.environ["TELEGRAM_TOKEN"],
            [
                GigaChatTest(ai=GigaChatNeuralNetwork(os.environ["GIGACHAT_AUTH_KEY"])),
                Review()
            ],
            db,
            admin_id=os.environ["ADMIN_ID"]
        ).run()
    finally:
        asyncio.run(db.close())