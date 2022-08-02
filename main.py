import discord
import os
import logging

client = discord.Client()


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


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    user_message = user_message.lower()
    channel = str(message.channel.name)
    print(f'{username}: {user_message} ({channel})')

    if message.author == client.user:
        return

    if message.channel.name == 'bot-text':
        if user_message.startswith('!add'):
            await message.channel.send(f'I added the bottle for {username}!')
            return
        elif user_message.startswith('!remove'):
            await message.channel.send(f'I removed the bottle for {username}!')
            return
        elif user_message.startswith('!list'):
            await message.channel.send(f'Here are all the bottles!')
            return
        elif user_message.startswith('!help'):
            await message.channel.send(f'My commands are !add, !remove, !list')
            return

print('Test Hallo Hallo Blöd')
logger = __init_logs()
client.run(os.environ.get("TOKEN", None))
