import discord
import config
from discord.ext import commands
from datetime import datetime, timedelta


'''
This class represents an "Event" object. An "Event" is defined as a scheduled, 
finite block of time, dedicated to a specific purpose. 
@authors: Nabil Cofie-Collison, Aymaan Bokth
'''
class Event:
    
    '''
    Constructs a new Event object with a specified name and group
    @param name The name of the Event
    @param group The group which the event is in
    '''
    def __init__(self, name, group) -> None:
        self.name = name
        self.group = group
        self.start_time = None
        self.end_time = None

    '''
    Specifies when an Event is
    @param year Year of Event
    @param month Month of Event
    @param day Day of Event
    @param start_hour Start hour of the Event
    @param start_minute Start minute of Event
    @param duration_minutes Total length of Event (in minutes)
    '''
    def createEvent(self, year, month, day, start_hour, start_minute, duration_minutes):
        start_datetime = datetime(year, month, day, start_hour, start_minute)
        end_datetime = start_datetime + timedelta(minutes=duration_minutes)
        self.start_time = start_datetime
        self.end_time = end_datetime

    '''
    Provides information regarding an Event's details
    @return Formatted string containing Event's name, group, start time, and end time
    '''
    def get_event_info(self):
        if self.start_time and self.end_time:
            return f"Event: {self.name} ({self.group.name}), Start: {self.start_time}, End: {self.end_time}"
        else:
            return "Event information is incomplete."
        
    
        
