import discord
from discord import app_commands
from discord.ext import commands
import config
import asyncio
import events
import groups
import members

'''
This is the main Class that implements the classes groups, members, and events
This class also functions as a GUI for the program.

'''

TOKEN = config.bot_token
client = commands.Bot(command_prefix="!", intents=discord.Intents.all())
all_users = []
all_groups = []


"""
Discord Event On_Ready Constructor to Initialize the Client.
Also initializes the tree commands for the program
"""


@client.event
async def on_ready():
    await client.tree.sync()
    print(f'{client.user} has connected to Discord!')

"""
This method is a command to create a new member and add them to a list.
It extracts the user's name from the interaction.
It creates a new member instance and appends it to the all_users list.
It responds with a message indicating that the user has been initialized.
"""


@client.tree.command(name="create_member", description="Creates Member")
async def create_member(interaction: discord.Interaction):
    user = interaction.user.name
    newM = members.Member(user)
    all_users.append(newM)
    await interaction.response.send_message(f'"{user}" has been initialized')

"""
This command creates a new group and adds the user as the first member.
It checks if the user is initialized before creating the group.
@param group_name The Name of the Group
"""
@client.tree.command(name="new_group", description="Create a group with the user a the only member ")
async def new_group(interaction: discord.Interaction, group_name: str):
    user = interaction.user.name
    mem = None
    for people in all_users:
        if people.name == user:
            mem = people
            break

    if mem is None:
        await interaction.response.send_message(f'"{user}" not initialized')
        return

    newG = groups.Group(group_name)
    mem.addGroup(newG)
    all_groups.append(newG)

    await interaction.response.send_message(f'New Group Created, <@{newG.name}>!')


"""
This command adds a user to an existing group,
checking for both the group's existence and the user's initialization.

@param group_name The Name of the Group
@param new_member The Name of the new user
"""
@client.tree.command(name="add_member_to_group", description="Adding Usersnames of people in a group")
async def add_member_to_group(interaction: discord.Interaction, group_name: str, new_member: str):

    group = None
    for existing_group in all_groups:  # Replace with your list of groups
        if existing_group.name == group_name:
            group = existing_group
            break

    if group is None:
        await interaction.response.send_message(f'Group "{group_name}" not found.')
        return

    mem = None
    for people in all_users:
        if people.name == new_member:
            mem = people
            break

    if mem is None:
        await interaction.response.send_message(f'"{new_member}" not initialized')
        return

    mem.addGroup(group)

    await interaction.response.send_message(f'"{new_member}" hase been added to "{group_name}"')

"""
This command adds a user to This command returns a list of groups that the user is a part of, checking if the user is initialized first.
existing group, checking for both the group's existence and the user's initialization.

"""
@client.tree.command(name="my_groups", description=" return the names and the users of groups you are a part of")
async def my_groups(interaction: discord.Interaction):
    user = interaction.user.name
    mem = None
    for people in all_users:
        if people.name == user:
            mem = people
            break

    if mem is None:
        await interaction.response.send_message(f'"{user}" not initialized')
        return

    groups = [group.name for group in mem.groups]
    group_info = '\n'.join([f'Group Name: {group}' for group in groups])
    await interaction.response.send_message(f'You are a part of the following groups:\n{group_info}')

"""
This command returns a schedule of events for the user, considering the user's group memberships.
It checks if the user is initialized before executing code
"""
@client.tree.command(name="my_schedule", description="return your schedule or a the events in your groups ")
async def my_schedule(interaction: discord.Interaction):
    user = interaction.user.name
    mem = None
    for people in all_users:
        if people.name == user:
            mem = people
            break

    if mem is None:
        await interaction.response.send_message(f'"{user}" not initialized')
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

"""
This command allows the user to add an event to an existing group, ensuring that the group exists.
@param group_name The Name of the Group
@param event_name The Name of the new event
@param year The Year of the new event
@param month The Month of the new event
@param day The Day of the new event
@param start_hour The Starting Hour of the new event
@param start_minute The Starting Minute of the new event
@param duration_minutes The Duration of the new event
"""
@client.tree.command(name="new_group_event", description="add event to group you are a part of")
async def new_group_event(interaction: discord.Interaction, group_name: str, event_name: str, year: int, month: int, day: int, start_hour: int, start_minute: int, duration_minutes: int):
    group = None
    for existing_group in all_groups:  # Replace with your list of groups
        if existing_group.name == group_name:
            group = existing_group
            break

    if group is None:
        await interaction.response.send_message(f'Group "{group_name}" not found.')
        return

    new_event = events.Event(event_name, group)
    new_event.createEvent(year, month, day, start_hour,
                          start_minute, duration_minutes)
    group.addEvent(new_event)

"""
This command allows the user to remove an event from an existing group,
verifying the group's existence and the event's presence.
It checks if the user is initialized before creating the group.
@param group_name The Name of the Group the event reside in
@param event_name The Name of the event being deleted
"""
@client.tree.command(name="remove_group_event", description="remove event to group you are a part of")
async def remove_group_event(interaction: discord.Interaction, group_name: str, event_name: str):
    group = None
    for existing_group in all_groups:  # Replace with your list of groups
        if existing_group.name == group_name:
            group = existing_group
            break

    if group is None:
        await interaction.response.send_message(f'Group "{group_name}" not found.')
        return

    event_to_remove = None
    for event in group.events:
        if event.name == event_name:
            event_to_remove = event
            break

    if event_to_remove:
        group.events.remove(event_to_remove)
        await interaction.response.send_message(f'Event "{event_name}" removed from group "{group_name}".')
    else:
        await interaction.response.send_message(f'Event "{event_name}" not found in group "{group_name}".')



client.run(TOKEN)
