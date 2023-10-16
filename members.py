import discord
import config
from discord.ext import commands


'''
Class defining a "Member" which represents a user interacting with the MeetupMentor discord bot.

'''
class Member:
    
    '''
    The constructor for creating a Member.
    @param self Variable representing a person/member
    @param name String being designated to the self parameter
    '''
    def __init__(self, name):
        self.name = name
        self.groups = []

    '''    
    Adds a member to a specified group given.
    @param self Variable representing a person/member
    @param group The group that a member is being added to
    @return The member being added into a group
    '''
    def addGroup(self, group):
        self.groups.append(group)
        group.addMember(self)
        
    
    '''
    Returns a representation of the group(s) that self/member is a part of.
    @param self Variable representing a person/member
    @return A formatted string representing the group(s) that member belongs to
    '''
    def get_member_info(self):
        group_names = [group.name for group in self.groups]
        return f"Member Name: {self.name}\nBelongs to Groups: {', '.join(group_names)}"

    '''
    Returns the group(s) that belong to the current self/member accessing the bot.
    @param self Variable representing a person/member
    @return The group name(s) for the member
    '''
    def get_group_names(self):
        return [group.name for group in self.groups]

    '''
    Returns a string representation of the self/member.
    @param self Variable representing a person/member
    @return A string representing the self/member
    '''
    def __str__(self):
        return self.name
