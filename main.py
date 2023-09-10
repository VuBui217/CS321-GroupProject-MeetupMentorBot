import discord

TOKEN = 'MTE1MDIxMjg4MzM4OTYxMjI0NA.GpxOk2.Ghyw7GqLoVLU9pP3oxMwnOeMYmxltHlO-7MQuE'
client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

client.run(TOKEN)