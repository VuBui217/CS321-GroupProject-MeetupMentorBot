import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timedelta
from discord.ui import View, Button
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os.path
import config
import asyncio
import events
import groups
import members
import logging


'''
This is the main Class that implements the classes groups, members, and events
This class also functions as a GUI for the program.

'''
creds = None
SCOPES = ["https://www.googleapis.com/auth/calendar"]

if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json",SCOPES)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

service = build("calendar", "v3", credentials=creds, static_discovery=False)
TOKEN = config.bot_token
client = commands.Bot(command_prefix="!", intents=discord.Intents.all())
all_users = []
all_groups = []
selected_date_button = None
selected_group_button = None


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
  Creates a URL that adds an event to Google Calendar.

  Args:
      event_name: The name of the event.
      start_datetime: A datetime object representing the start time of the event.
      end_datetime: (Optional) A datetime object representing the end time of the event (defaults to 30 minutes after start).

  Returns:
      A URL that, when clicked, adds the event to the user's Google Calendar.
  """        
@client.tree.command(name="google_link", description="Which event are you interested in? (Enter event number or name)'")
async def create_google_calendar_event_url(interaction: discord.Interaction, event_index: int): 
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
            schedule.append(event)

    
    
    
        
    event_index-=1 
    if event_index < 0 or event_index >= len(schedule):
        await interaction.response.send_message(f"Invalid event selection. Please try again.")
        return    
    gevent = schedule[event_index]
        
    

    # Base URL for Google Calendar event creation
    base_url = "https://calendar.google.com/calendar/render?action=edit"

    # Encode event details
    encoded_name = gevent.name.replace(" ", "%20")
    start_time_param = f"dates={gevent.start_time.strftime('%Y%m%dT%H%M%SZ')}"
    end_time_param = f"end={gevent.end_time.strftime('%Y%m%dT%H%M%SZ')}"


    # Combine URL parts
    url = f"{base_url}&text={encoded_name}&{start_time_param}&{end_time_param}"


    await interaction.response.send_message(f"Click this link to add the event to your Google Calendar: {url}")
           


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

   
    group.addEvent(year, event_name, month, day, start_hour,
                          start_minute, duration_minutes)
    
    await interaction.response.send_message(f'New Event Created, <@{event_name}>!')

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
  
  
  
async def process_selections(selected_date, selected_group):
    # Save selected buttons to global variables
    selected_date_button = datetime.strptime(selected_date, "%Y-%m-%d")
    
    
    for existing_group in all_groups:  # Replace with your list of groups
        if existing_group.name == selected_group:
            selected_group_button = existing_group
            break

        
class ChooseDateGroupView(View):
    def __init__(self, user_groups):
        super().__init__(timeout=60)

        self.selected_date = None
        self.selected_group = None

        current_date = datetime.now()
        for i in range(7):
            date_id = f"date-{current_date.strftime('%Y-%m-%d')}"
            button = discord.ui.Button(
                label=f"{current_date.month}-{current_date.day}",
                style=discord.ButtonStyle.blurple,
                custom_id=date_id,
            )
            self.add_item(button)
            current_date += timedelta(days=1)

        for group in user_groups:
            button = discord.ui.Button(
                label=group.name, style=discord.ButtonStyle.green, custom_id=group.id
            )
            self.add_item(button)

    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user == interaction.message.author

    async def on_button_click(self, interaction: discord.Interaction, button: Button,):
        if button.custom_id.startswith("date-"):
            self.selected_date = button.custom_id
        else:
            self.selected_group = button.label

        # Check if both selections are made
        if self.selected_date and self.selected_group:
            self.stop()
            await interaction.message.edit(content="Selections confirmed!")
            # Process selections here (call another function, etc.)
            # You can access user and user_groups via `self`
            await process_selections(self.selected_date, self.selected_group)
            
    

       
"""
    This command allows the user to create and name 30 min 
    meeting between 9 and 7.

    @param group_name: The Name of the New Event
    
    """
@client.tree.command(name="schedule_meeting", description="Schedule a 30-minute meeting")
async def schedule_meeting(interaction: discord.Interaction,event_name: str):
    user = interaction.user.name # Get the user who invoked the command
    current_date = datetime.now()

    # Get the user's groups
    user = None
    for people in all_users:
        if people.name == user:
            mem = people
            break
    
    if mem is None:
        await interaction.response.send_message(f'"{user}" not initialized')
        return
    
        
    user_groups = mem.groups
    view = ChooseDateGroupView(user, user_groups)
    await interaction.response.send_message("Select a date and a group for a meeting between 9 and 7 :", view=view)

    # Get the selected date and group
    selected_date = selected_date_button
    selected_group = selected_group_button
    
    selected_date_button = None
    selected_group_button = None

    # Find a 30-minute interval where all members are free

    if selected_group is not None:
        # Call a function to find a 30-minute interval in the selected group's schedule
        free_interval = selected_group.find_free_interval(selected_date_button,event_name)
    interaction.response.send_message(free_interval)



client.run(TOKEN)
