import pytest
from datetime import datetime, timedelta
from events import Event

# Init group


class EventGroupTest:
    def __init__(self, name):
        self.name = name

# Test the Event class


def test_event_creation():
    # Create a group
    group = EventGroupTest("Test Group")

    # Create an event
    event = Event("Test Event", group)

    # Set event details
    event.createEvent(2023, 1, 1, 12, 0, 60)

    # Check if the event details are set correctly
    assert event.name == "Test Event"
    assert event.group == group
    assert isinstance(event.start_time, datetime)
    assert isinstance(event.end_time, datetime)


def test_get_event_info():
    # Create a group
    group = EventGroupTest("Test Group")

    # Create an event
    event = Event("Test Event", group)

    # Set event details
    event.createEvent(2023, 1, 1, 12, 0, 60)

    # Check if get_event_info() returns the correct formatted string
    expected_info = f"Event: Test Event (Test Group), Start: {event.start_time}, End: {event.end_time}"
    assert event.get_event_info() == expected_info


def test_incomplete_event_info():
    # Create a group
    group = EventGroupTest("Test Group")

    # Create an event without setting event details
    event = Event("Test Event", group)

    # Check if get_event_info() returns the correct string for incomplete information
    assert event.get_event_info() == "Event information is incomplete."


def test_event_info_without_end_time():
    # Create a group
    group = EventGroupTest("Test Group")

    # Create an event without setting end time
    event = Event("Test Event", group)
    event.createEvent(2023, 1, 1, 12, 0, 60)
    event.end_time = None

    # Check if get_event_info() returns the correct string for an event without end time
    expected_info = f"Event: Test Event (Test Group), Start: {event.start_time}, End: None"
    assert event.get_event_info() == expected_info


def test_event_info_without_start_time():
    # Create a group
    group = EventGroupTest("Test Group")

    # Create an event without setting start time
    event = Event("Test Event", group)
    event.createEvent(2023, 1, 1, 12, 0, 60)
    event.start_time = None

    # Check if get_event_info() returns the correct string for an event without start time
    expected_info = "Event: Test Event (Test Group), Start: None, End: 2023-01-01 13:00:00"
    assert event.get_event_info() == expected_info


def test_event_info_with_invalid_dates():
    # Create a group
    group = EventGroupTest("Test Group")

    # Create an event with invalid dates
    event = Event("Test Event", group)
    event.createEvent(2023, 13, 32, 25, 70, 60)

    # Check if get_event_info() returns the correct string for an event with invalid dates
    assert event.get_event_info() == "Event information is incomplete."


def test_event_info_with_negative_duration():
    # Create a group
    group = EventGroupTest("Test Group")

    # Create an event with negative duration
    event = Event("Test Event", group)
    event.createEvent(2023, 1, 1, 12, 0, -30)

    # Check if get_event_info() returns the correct string for an event with negative duration
    assert event.get_event_info() == "Event information is incomplete."


def test_event_info_with_zero_duration():
    # Create group
    group = EventGroupTest("Test Group")

    # Create an event with zero duration
    event = Event("Test Event", group)
    event.createEvent(2023, 1, 1, 12, 0, 0)

    # Check if get_event_info() returns the correct string for an event with zero duration
    assert event.get_event_info() == "Event information is incomplete."


def test_event_info_with_valid_dates():
    # Create a group
    group = EventGroupTest("Test Group")

    # Create an event with valid dates
    event = Event("Test Event", group)
    event.createEvent(2023, 12, 31, 23, 59, 1)

    # Check if get_event_info() returns the correct formatted string for an event with valid dates
    expected_info = f"Event: Test Event (Test Group), Start: 2023-12-31 23:59:00, End: 2024-01-01 00:00:00"
    assert event.get_event_info() == expected_info
