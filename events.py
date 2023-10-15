import discord
import config
from discord.ext import commands
from datetime import datetime, timedelta



class Event:

    def __init__(self, name, group) -> None:
        self.name = name
        self.group = group
        self.start_time = None
        self.end_time = None

    def createEvent(self, year, month, day, start_hour, start_minute, duration_minutes):
        start_datetime = datetime(year, month, day, start_hour, start_minute)
        end_datetime = start_datetime + timedelta(minutes=duration_minutes)
        self.start_time = start_datetime
        self.end_time = end_datetime

    def get_event_info(self):
        if self.start_time and self.end_time:
            return f"Event: {self.name} ({self.group.name}), Start: {self.start_time}, End: {self.end_time}"
        else:
            return "Event information is incomplete."
        
