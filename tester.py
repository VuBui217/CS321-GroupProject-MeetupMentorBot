import unittest
from groups.py import __init__
from groups.py import addMember
from groups.py import addEvent

class initUnitTests(unittest.TestCase):
    #idk if this is right
    def test_init_name (self):
        result = __init__("first", "last")
        self.assertEqual(result, "first last")

class addMemberUnitTests(unittest.TestCase):


class addEventUnitTests(unittest.TestCase):