import discord
import config
from discord.ext import commands


class Member:
    
    def __init__(self,name) -> None:
        self.name = name
        self.groups = []
        
    def addGroup(self, Group ) :
        self.members.append(Group())
        return self
        
class Event:
    
    def __init__(self,name) -> None:
        self.name = name
        self.groups = []
        


class Group:
    
    def __init__(self,name) -> None:
        self.name = name
        self.members = []
        self.events =[]
        
    def addMember(self, member):
        self.members.append(member.addGroup(self))
        
        
    def addEvent(self):
        self.events.append(Event())