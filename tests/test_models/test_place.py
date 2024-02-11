#!/usr/bin/python3
"""Defines unittests for models/place.py.

Unittest classes:
    TestPlace_instantiation
    TestPlace_save
    TestPlace_to_dict
"""
import unittest
from models.place import Place
from models.base_model import BaseModel


class TestPlaceInstantiation(unittest.TestCase):
    def test_instantiation(self):
        place = Place()
        self.assertIsInstance(place, BaseModel)
        self.assertIsInstance(place, Place)


class TestPlaceSave(unittest.TestCase):
    def test_save(self):
        place = Place()
        place.save()
        self.assertNotEqual(place.created_at, place.updated_at)


class TestPlaceToDict(unittest.TestCase):
    def test_to_dict(self):
        place = Place()
        place_dict = place.to_dict()
        self.assertIsInstance(place_dict, dict)
        self.assertIn('__class__', place_dict)
        self.assertEqual(place_dict['__class__'], 'Place')


if __name__ == '__main__':
    unittest.main()
