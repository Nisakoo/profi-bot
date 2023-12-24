import os
import asyncio

from dotenv import load_dotenv

from bot.telegram.bot import TelegramBot
from neural_network.gigachat import GigaChatNeuralNetwork
from db.sqlite3_db import Sqlite3DataBase


if __name__ == "__main__":
    load_dotenv()

    db = Sqlite3DataBase(filename=os.environ["DATABASE_FILE"])
    loop = asyncio.get_event_loop()
    loop.run_until_complete(db.connect())

    try:
        TelegramBot(
            os.environ["TELEGRAM_TOKEN"],
            GigaChatNeuralNetwork(os.environ["GIGACHAT_AUTH_KEY"]),
            db
        ).run()
    finally:
        asyncio.run(db.close())