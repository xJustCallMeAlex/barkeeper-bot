import asyncio
import uuid

import os
import logging
from discord.ext import commands
import asyncpg
from dataclasses import dataclass


async def run():
    db = await asyncpg.create_pool(os.environ.get("DATABASE_URL", None), max_size=5, min_size=3)
    bot = Bot(db)
    await bot.start(os.environ.get("TOKEN", None))


class Bot(commands.Bot):
    def __init__(self, db):
        super().__init__(command_prefix='???.?')
        self.db = db

    # @client.event
    async def on_ready(self):
        print('We have logged in as {0.user}'.format(self))

    async def on_message(self, message):
        await self.process_commands(message)
        username = str(message.author).split('#')[0]
        user_message = str(message.content)
        if message.channel.name == 'alkoholregal':
            if user_message.startswith('!add:'):
                user_message = user_message.split(':')[1]
                user_message = user_message.strip()
                await self.db.execute(f"""
                               INSERT INTO drinks(drink_id, name) VALUES (gen_random_uuid(), '{user_message}');
                           """)
                await message.channel.send(f'{user_message} has been added to the shelf by {username}')
                return
            elif user_message.startswith('!remove:'):
                user_message = user_message.split(':')[1]
                user_message = user_message.strip()
                await self.db.execute(f"""
                                DELETE FROM drinks WHERE name = '{user_message}';
                            """)
                await message.channel.send(f'{user_message} has been removed from the shelf by {username}')
                return
            elif user_message.startswith('!list'):
                result_set = await self.db.fetch(f"""
                                SELECT drink_id, name
                                FROM drinks
                                ORDER BY drink_id;
                            """)
                drink_list = [str(Drink(*result)) for result in result_set]
                await message.channel.send('This is a list of all the Bottles')
                await message.channel.send("\n".join(drink_list))
                return
            elif user_message.startswith('!help'):
                await message.channel.send("""
This is a list of all the commands.
!add: bottlename - This command adds a bottle to the shelf.
!remove: bottlename - This command removes a bottle from the shelf. 
!list - This command lists the whole content of the shelf. 
!help - This command shows the help menu

Important is that the bottlename does not contain ':'. 
Because the colon is used to split the message string.

This bot was programmed by Alexander Kolar with the help of Johannes Riedmann (aka Luigi-Fan).
I hope you enjoy!
                        """)
                return
        print(message.content)


class CustomFormatter(logging.Formatter):
    grey = "\x1b[00;20m"
    green = "\x1b[32;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    err_format = "%(levelname)s: %(asctime)s - %(message)-90s"
    format = err_format + " \t[%(name)s] (in: %(filename)s, line %(lineno)d)"
    date_format = "%Y-%m-%d %H:%M:%S"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: green + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + err_format + reset,
        logging.CRITICAL: bold_red + err_format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt=self.date_format)
        return formatter.format(record)


def __init_logs():
    handler = logging.StreamHandler()
    handler.setFormatter(CustomFormatter())

    logs = logging.getLogger('discord')
    logs.addHandler(handler)
    logs.setLevel(logging.INFO)
    return logs


@dataclass(frozen=True)
class Drink:
    drink_id: uuid.UUID
    name: str

    def __str__(self):
        return self.name


loop = asyncio.get_event_loop()
loop.run_until_complete(run())
logger = __init_logs()
