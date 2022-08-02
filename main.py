import discord
import os

client = discord.Client()

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
client.run(os.environ.get("TOKEN", None))
