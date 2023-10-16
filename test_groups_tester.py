import pytest
import events
import members
import groups

def test_add_multiple_members():
    group1 = groups.Group("test_group")
    member1 = "Hayder"
    member2 = "Lily"
    member3 = "Nabil"
    group1.addMember(member1)
    group1.addMember(member2)
    group1.addMember(member3)
    assert group1.members == [member1, member2, member3]
    

def test_add_multiple_events():
    group1 = groups.Group("test_group")
    
    group1.addEvent("Baseball", 10, 15, 15, 30, 60)
    group1.addEvent("Study Session", 3, 10, 10, 30, 120)
    group1.addEvent("Exam", 3, 10, 12, 0, 90)
    
    bbEvent = events.Event("Baseball")
    bbEvent.createEvent(10, 15, 15, 30, 60)
    
    studySessionEvent = events.Event("Study Session")
    studySessionEvent.createEvent(3, 10, 10, 30, 120)
    
    examEvent = events.Event("Exam")
    examEvent.createEvent(3, 10, 12, 0, 90)
    
    assert group1.events == [bbEvent, studySessionEvent, examEvent]
    

def test_remove_multiple_events():
    group1 = groups.Group("test_group")
    
    group1.addEvent("Baseball", 10, 15, 15, 30, 60)
    group1.addEvent("Study Session", 3, 10, 10, 30, 120)
    group1.addEvent("Exam", 3, 10, 12, 0, 90)
    
    bbEvent = events.Event("Baseball")
    bbEvent.createEvent(10, 15, 15, 30, 60)
    
    studySessionEvent = events.Event("Study Session")
    studySessionEvent.createEvent(3, 10, 10, 30, 120)
    
    examEvent = events.Event("Exam")
    examEvent.createEvent(3, 10, 12, 0, 90)
    
    group1.removeEvent(bbEvent)
    group1.removeEvent(examEvent)
    
    assert group1.events == [studySessionEvent]