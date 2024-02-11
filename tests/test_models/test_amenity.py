#!/usr/bin/python3
"""Defines unittests for models/amenity.py.

Unittest classes:
    TestAmenity_instantiation
    TestAmenity_save
    TestAmenity_to_dict
"""
import unittest
from models.amenity import Amenity
from models.base_model import BaseModel


class TestAmenityInstantiation(unittest.TestCase):
    def test_instantiation(self):
        amenity = Amenity()
        self.assertIsInstance(amenity, BaseModel)
        self.assertIsInstance(amenity, Amenity)


class TestAmenitySave(unittest.TestCase):
    def test_save(self):
        amenity = Amenity()
        amenity.save()
        self.assertNotEqual(amenity.created_at, amenity.updated_at)


class TestAmenityToDict(unittest.TestCase):
    def test_to_dict(self):
        amenity = Amenity()
        amenity_dict = amenity.to_dict()
        self.assertIsInstance(amenity_dict, dict)
        self.assertIn('__class__', amenity_dict)
        self.assertEqual(amenity_dict['__class__'], 'Amenity')


if __name__ == '__main__':
    unittest.main()
