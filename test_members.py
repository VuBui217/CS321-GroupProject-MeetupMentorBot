import pytest
import events
import members
from members import Member
from groups import Group

def test_initialization():
    member1 = Member("First member")
    assert member1.name == "First member"

def test_check_if_no_groups():
    member1 = Member("First member")
    assert member1.get_member_info() == "Member Name: " + member1.name + "\nBelongs to Groups: "

def test_check_group():
    member1 = Member("First member")
    group1 = Group("First group")
    member1.addGroup(group1)
    assert member1.get_member_info() == "Member Name: " + member1.name + "\nBelongs to Groups: " + group1.name

def test_check_groups():
    member1 = Member("First member")
    group1 = Group("First group")
    group2 = Group("Second group")
    member1.addGroup(group1)
    member1.addGroup(group2)
    assert member1.get_member_info() == "Member Name: " + member1.name + "\nBelongs to Groups: " + group1.name + ", " + group2.name

#Still being worked on
def test_get_group_names():
    member1 = Member("First member")
    group1 = Group("First group")
    member1.addGroup(group1)
    assert member1.get_group_names == [group1.name]

def test_check_string():
    member1 = Member("First member")
    assert member1.__str__ == member1.__str__
