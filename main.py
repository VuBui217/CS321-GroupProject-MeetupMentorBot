import discord
import config
from discord.ext import commands
import os

TOKEN = config.bot_token
client = commands.Bot(command_prefix ="!", intents=discord.Intents.all())


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.tree.command(name ="create_group", description="Adding Usersnames of people in a group")
async def create_group(interaction: discord.Interaction):

    print(f'Place Holder for Adding Usersnames of people in a group to a list and then storring its a list in MongoDb')

@client.command()
async def my_groups(ctx):
    print(f'Place Holder for return the names and the users of groups you are a part of ')

@client.command()
async def my_schedule(ctx):
    print(f'Place Holder for return your schedule')


@client.command()
async def add_my_event(ctx):
    print(f'Place Holder to add event on your schedule')
    
@client.command()
async def add_group_event(ctx):
    print(f'Place Holder to add event on every member on your groups schedule')

@client.command()
async def remove_group_event(ctx):
    print(f'Place Holder to remove event on every member on your groups schedule')

@client.command()
async def remove_my_event(ctx):
    print(f'Place Holder to remove event on your schedule')


client.run(TOKEN)

