
import pytest
import events
import members
from groups import Group


# Define test cases


def test_group_initialization():
    group1 = Group("Test Group")
    assert group1.name == "Test Group"
    assert group1.members == []
    assert group1.events == []


def test_add_member():
    group1 = Group("Test Group")
    member_name = "John"
    group1.addMember(member_name)
    assert group1.members == [member_name]


def test_add_event():
    group1 = Group("Test Group")
    event_name = "Test Event"
    group1.addEvent(event_name, year=2023, month=10, day=15,
                    startHour=15, startMin=30, duration=60)
    assert len(group1.events) == 1
    event = group1.events[0]
    assert event.name == event_name


def test_multiple_groups():
    group1 = Group("Group 1")
    group2 = Group("Group 2")

    # Check group names
    assert group1.name == "Group 1"
    assert group2.name == "Group 2"

    # Ensure groups have different member lists
    member1_group1 = "Vu"
    member1_group2 = "VuVu"
    group1.addMember(member1_group1)
    group2.addMember(member1_group2)
    assert group1.members == [member1_group1]
    assert group2.members == [member1_group2]


def test_multiple_events():
    group1 = Group("Test Group 1")

    event1_name = "Event 1"
    event2_name = "Event 2"

    group1.addEvent(event1_name, year=2023, month=10, day=15,
                    startHour=15, startMin=30, duration=60)
    group1.addEvent(event2_name, year=2023, month=11, day=20,
                    startHour=18, startMin=0, duration=90)

    # Check the number of events in the group
    assert len(group1.events) == 2

    # Check event names
    assert group1.events[0].name == event1_name
    assert group1.events[1].name == event2_name
