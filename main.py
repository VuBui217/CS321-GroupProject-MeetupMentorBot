import discord
from discord import app_commands
from discord.ext import commands
import config
import os
import events
import groups
import members


TOKEN = config.bot_token
client = commands.Bot(command_prefix="!", intents=discord.Intents.all())
all_users = []
all_groups = []

client.synced = False
client.added = False

@client.event
async def on_ready():
    await client.wait_until_ready()
    if not client.synced:
        await client.tree.sync(guild = discord.Object(id =1143632695503638528))
        client.synced = True
    if not client.added:
      client.added = True   
    print(f'{client.user} has connected to Discord!')


@client.tree.command(name="create_member", description="Creates Member")
async def create_member(interaction: discord.Interaction):
    user = interaction.user.name
    newM = members.Member(user)
    all_users.append(newM)
    await interaction.response.send_message(f'"{user}" has been initialized')


@client.tree.command(name="create_group", description="Create a group with the user a the only member ")
async def create_group(interaction: discord.Interaction, GroupName: str):
    user = interaction.user.name
    mem = None
    for people in all_users:
        if people.name == user:
            mem = people
            break

    if mem is None:
        await interaction.response.send_message(f'"{user}" not initialized')
        return

    newG = groups.Group(GroupName)
    mem.addGroup(newG)
    all_groups.append(newG)

    await interaction.response.send_message(f'New Group Created, <@{newG.name}>!')


@client.tree.command(name="add_member_group", description="Adding Usersnames of people in a group")
async def add_member_group(interaction: discord.Interaction, GroupName: str, newUser: str):

    group = None
    for existing_group in all_groups:  # Replace with your list of groups
        if existing_group.name == GroupName:
            group = existing_group
            break

    if group is None:
        await interaction.response.send_message(f'Group "{GroupName}" not found.')
        return

    mem = None
    for people in all_users:
        if people.name == newUser:
            mem = people
            break

    if mem is None:
        await interaction.response.send_message(f'"{newUser}" not initialized')
        return

    mem.addGroup(group)

    await interaction.response.send_message(f'"{newUser}" hase been added to "{GroupName}"')


@client.tree.command(name="my_groups", description=" return the names and the users of groups you are a part of")
async def my_groups(interaction: discord.Interaction):
    user = interaction.user.name
    mem = None
    for people in all_users:
        if people.name == user:
            mem = people
            break
        
    if mem is None:
        await  interaction.response.send_message(f'"{user}" not initialized')
        return
    
    groups = [group.name for group in mem.groups]
    group_info = '\n'.join([f'Group Name: {group}' for group in groups])
    await interaction.response.send_message(f'You are a part of the following groups:\n{group_info}')


@client.tree.command(name="my_schedule", description="return your schedule or a the events in your groups ")
async def my_schedule(interaction: discord.Interaction):
    user = interaction.user.name
    mem = None
    for people in all_users:
        if people.name == user:
            mem = people
            break
        
    if mem is None:
        await  interaction.response.send_message(f'"{user}" not initialized')
        return
    
    schedule = []
    
    for group in mem.groups:
        for event in group.events:
            schedule.append(event.get_event_info())

    if not schedule:
        await interaction.response.send_message('No events in your schedule or groups.')
    else:
        schedule_info = '\n'.join(schedule)
        await interaction.response.send_message(f'Your schedule:\n{schedule_info}')


@client.tree.command(name="add_group_event", description="add event to group you are a part of")
async def add_group_event(interaction: discord.Interaction,GroupName: str, event_name: str, year: int, month: int, day: int, start_hour: int, start_minute: int, duration_minutes: int):
    group = None
    for existing_group in all_groups:  # Replace with your list of groups
        if existing_group.name == GroupName:
            group = existing_group
            break

    if group is None:
        await interaction.response.send_message(f'Group "{GroupName}" not found.')
        return

    
    new_event = events.Event(event_name, group)
    new_event.createEvent(year, month, day, start_hour, start_minute, duration_minutes)
    group.addEvent(new_event)


@client.tree.command(name="remove_group_event", description="remove event to group you are a part of")
async def remove_group_event(interaction: discord.Interaction,GroupName: str, EventName: str):
    group = None
    for existing_group in all_groups:  # Replace with your list of groups
        if existing_group.name == GroupName:
            group = existing_group
            break

    if group is None:
        await interaction.response.send_message(f'Group "{GroupName}" not found.')
        return
    
    event_to_remove = None
    for event in group.events:
        if event.name == EventName:
            event_to_remove = event
            break

    if event_to_remove:
        group.events.remove(event_to_remove)
        await interaction.response.send_message(f'Event "{EventName}" removed from group "{GroupName}".')
    else:
        await interaction.response.send_message(f'Event "{EventName}" not found in group "{GroupName}".') 


client.run(TOKEN)
