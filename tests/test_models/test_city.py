#!/usr/bin/python3
"""Defines unittests for models/city.py.

Unittest classes:
    TestCity_instantiation
    TestCity_save
    TestCity_to_dict
"""
import unittest
from models.base_model import BaseModel
from models.city import City
from datetime import datetime


class TestCity(unittest.TestCase):
    def test_city_inheritance(self):
        city = City()
        self.assertIsInstance(city, BaseModel)
        self.assertTrue(hasattr(city, "id"))
        self.assertTrue(hasattr(city, "created_at"))
        self.assertTrue(hasattr(city, "updated_at"))

    def test_city_attributes(self):
        city = City()
        self.assertTrue(hasattr(city, "state_id"))
        self.assertTrue(hasattr(city, "name"))

    def test_city_attribute_types(self):
        city = City()
        self.assertIsInstance(city.state_id, str)
        self.assertIsInstance(city.name, str)

    def test_city_updated_at_type(self):
        city = City()
        self.assertIsInstance(city.updated_at, datetime)

    def test_city_created_at_type(self):
        city = City()
        self.assertIsInstance(city.created_at, datetime)


if __name__ == '__main__':
    unittest.main()
