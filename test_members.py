import pytest
import events
import members
from members import Member
from groups import Group

def test_initialization():
    member1 = Member("First member")
    assert member1.name == "First member"

def test_member_string():
    test_member = Member("Test member")
    assert str(test_member) == test_member.name

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

def test_add_group():
    test_member = Member("Test Member")
    test_group = Group("First Group")
    test_member.addGroup(test_group)
    assert test_group in test_member.groups
    assert test_member in test_group.members

def test_get_no_group_names():
    test_member = Member("Test member")
    assert test_member.get_group_names() == []

def test_get_group_names():
    test_member = Member("Test member")
    test_group = Group("First group")
    test_member.addGroup(test_group)
    assert test_member.get_group_names() == [test_group.name]

def test_get_multiple_group_names():
    member1 = Member("First member")
    group1 = Group("First group")
    group2 = Group("Second group")
    member1.addGroup(group1)
    member1.addGroup(group2)
    assert member1.get_group_names() == [group1.name, group2.name]
