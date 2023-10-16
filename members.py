import discord
import config
from discord.ext import commands



class Member:
    
    def __init__(self, name):
        self.name = name
        self.groups = []
        
    def addGroup(self, group):
        self.groups.append(group)
        group.addMember(self)
        

    def get_member_info(self):
        group_names = [group.name for group in self.groups]
        return f"Member Name: {self.name}\nBelongs to Groups: {', '.join(group_names)}"

    def get_group_names(self):
        return [group.name for group in self.groups]

    def __str__(self):
        return self.name
