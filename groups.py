import discord
import config
from discord.ext import commands
from datetime import time , date


class Member:
    
    def __init__(self,name) -> None:
        self.name = name
        self.groups = []
        
    def addGroup(self, group:Group ) :
        self.groups.append(Group())
        return self
        
class Event:
    
    def __init__(self,name, group) -> None:
        self.name = name
        self.groups = group
        self.date = date.today()
        self.startTime = time(0,0,0)
        self.endTime = time(0,0,0)
        
    def createEvent(self, month, day, startHour, startMin, duration):
        self.date.month = month
        self.date.day = day
        self.startTime.hour = startHour
        self.startTime.min = startMin
        self.endTime = self.startTime
        temp = startMin + duration 
        if (temp > 59):
            
            while(temp > 59):
                temp -= 60
                self.endTime.hour +=1
                
        self.endTime.min = temp
            
        
        


    
        
        


class Group:
    
    def __init__(self,name) -> None:
        self.name = name
        self.members = []
        self.events =[]
        
    def addMember(self, member: Member):
        
        self.members.append(member.addGroup(self))
        
        
    def addEvent(self,eventName,month, day, startHour, startMin, duration):
        tempEvent = Event(eventName, self.name)
        tempEvent.createEvent(month, day, startHour, startMin, duration)
        self.events.append(tempEvent)