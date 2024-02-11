#!/usr/bin/python3
"""Defines unittests for models/state.py.

Unittest classes:
    TestState_instantiation
    TestState_save
    TestState_to_dict
"""
import unittest
from models.state import State
from models import storage


class TestStateInstantiation(unittest.TestCase):
    def test_instantiation(self):
        state = State()
        self.assertTrue(isinstance(state, State))
        self.assertEqual(state.name, "")


class TestStateSave(unittest.TestCase):
    def test_save(self):
        state = State()
        state.name = "California"
        state.save()
        key = "State." + state.id
        obj_dict = storage.all()["State"]
        self.assertTrue(key in obj_dict)
        self.assertEqual(obj_dict[key].to_dict(), state.to_dict())


class TestStateToDict(unittest.TestCase):
    def test_to_dict(self):
        state = State()
        state.name = "New York"
        state_dict = state.to_dict()
        self.assertEqual(state_dict["name"], "New York")
        self.assertEqual(state_dict["__class__"], "State")


if __name__ == "__main__":
    unittest.main()
