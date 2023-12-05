import discord
import config
from discord.ext import commands
from datetime import datetime, timedelta
import events
import members

"""
Class to represents a group in the discord bot. group of people that want to mange their time and tasks.

"""
class Group:
    
    """
    Construct Group with the group name, group member names and the events.
    @param name The name of the group.
    """
    def __init__(self, name) -> None:
        self.name = name
        self.members = []
        self.events = []

    """
    This method will add new member to the group.
    @param member (members.Member): the new member that going to be added to the group.
    """
    def addMember(self, member: members.Member):

        self.members.append(member)
        
    """
    Method to add new event to the group. 
    @param eventName The name of the event.
    @param year The year of the event.
    @param month The month of the event.
    @param day The day of the event.
    @param startHour The starting hour of the event.
    @param startMin  The starting minute of the event.
    @param duration The duration of the event in minutes.
    """
    def addEvent(self,year, eventName, month, day, startHour, startMin, duration):
        tempEvent = events.Event(eventName, self)
        tempEvent.createEvent(year,month, day, startHour, startMin, duration)
        self.events.append(tempEvent)


    """
    method to remove an event from the group.
    @param event the event thats going to be deleted. 
    """
    def removeEvent(self, event):
        if event in self.events:
            self.events.remove(event)
            
    def find_free_interval(self, start_datetime,name):
        # Define the start time and end time for the search interval
        search_start_time = datetime.combine(start_datetime.date(), datetime.strptime("09:00", "%H:%M").time())
        search_end_time = datetime.combine(start_datetime.date(), datetime.strptime("21:00", "%H:%M").time())

        current_time = search_start_time

        while current_time < search_end_time:
            # Check if there's an event in the group at the current time
            if any(event.start_time <= current_time < event.end_time for event in self.events):
                current_time += timedelta(minutes=30)
                continue

            # Check if any member of the group has an event at the current time
            all_members_free = all(
                not any(
                    event.start_time <= current_time < event.end_time
                    for group in member.groups
                    for event in group.events
                )
                for member in self.members
            )

            if all_members_free:
                # Call the method to add a new event to the group
                self.addEvent(self,current_time.year, name, current_time.month, current_time.day, current_time.hour, current_time.min, 30)
                return "New Event " + name + "starts at " + current_time.strftime("%I:%M %p")  # Return the formatted time

            current_time += timedelta(minutes=30)

        return None  # If no free interval is found

