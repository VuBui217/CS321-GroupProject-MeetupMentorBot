import discord
import config
from discord.ext import commands
import events
import members


class Group:

    def __init__(self, name) -> None:
        self.name = name
        self.members = []
        self.events = []

    def addMember(self, member: members.Member):

        self.members.append(member)
        

    def addEvent(self, eventName, month, day, startHour, startMin, duration):
        tempEvent = events.Event(eventName, self)
        tempEvent.createEvent(month, day, startHour, startMin, duration)
        self.events.append(tempEvent)
     
        
    def removeEvent(self, event):
        if event in self.events:
            self.events.remove(event)
