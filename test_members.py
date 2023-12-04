import pytest
import events
import members
from members import Member

def test_initialization():
    member1 = Member("First member")
    assert member1.name == "First member"

def test_check_if_no_groups():
    member1 = Member("First member")
    assert member1.get_member_info() == "Member Name: " + member1.name + "\nBelongs to Groups: "

def test_check_groups():
    member1 = Member("First member")
    