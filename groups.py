import discord
import config
from discord.ext import commands
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

    def addEvent(self, eventName, year, month, day, startHour, startMin, duration):
        tempEvent = events.Event(eventName, self)
        tempEvent.createEvent(year, month, day, startHour, startMin, duration)
        self.events.append(tempEvent)

    """
    method to remove an event from the group.
    @param event the event thats going to be deleted. 
    """

    def removeEvent(self, event):
        if event in self.events:
            self.events.remove(event)
