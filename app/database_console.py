import os
import sys
import csv
import asyncio

import aiosqlite
from dotenv import load_dotenv


async def send_commands(database: str) -> None:
    async with aiosqlite.connect(database) as db:

        while True:
            sql = input(">>> ")
            async with db.execute(sql) as cursor:
                print("OUTPUT: ")
                async for row in cursor:
                    print(row)


async def db_to_csv(database: str) -> None:
    async with aiosqlite.connect(database) as db:
        async with db.execute("SELECT * FROM events") as cursor:
            with open("data.csv", "w", newline="", encoding="utf-8") as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow([i[0] for i in cursor.description])
                
                async for row in cursor:
                    csv_writer.writerow(row)


if __name__ == "__main__":
    load_dotenv()

    try:
        args = sys.argv

        if len(args) == 2:
            if args[1] == "console":
                asyncio.run(send_commands(os.environ["DATABASE_FILE"]))
            elif args[1] == "csv":
                asyncio.run(db_to_csv(os.environ["DATABASE_FILE"]))
    finally:
        print("\n\nBye.")