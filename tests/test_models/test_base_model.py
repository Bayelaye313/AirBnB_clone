#!/usr/bin/python3
"""Defines unittests for models/base_model.py.

Unittest classes:
    TestBaseModel_instantiation
    TestBaseModel_save
    TestBaseModel_to_dict
"""
import unittest
from models.base_model import BaseModel


class TestBaseModelInstantiation(unittest.TestCase):
    def test_instantiation(self):
        model = BaseModel()
        self.assertIsInstance(model, BaseModel)
        self.assertIsNotNone(model.id)
        self.assertIsNotNone(model.created_at)
        self.assertIsNotNone(model.updated_at)


class TestBaseModelSave(unittest.TestCase):
    def test_save(self):
        model = BaseModel()
        old_updated_at = model.updated_at
        model.save()
        new_updated_at = model.updated_at
        self.assertNotEqual(old_updated_at, new_updated_at)


class TestBaseModelToDict(unittest.TestCase):
    def test_to_dict(self):
        model = BaseModel()
        model_dict = model.to_dict()
        self.assertIsInstance(model_dict, dict)
        self.assertIn('__class__', model_dict)
        self.assertEqual(model_dict['__class__'], 'BaseModel')


class TestBaseModel_str(unittest.TestCase):
    """Test cases for the __str__ method of the BaseModel class."""

    def test_str_output(self):
        """Test the string representation of the BaseModel instance."""
        test_instance = BaseModel()
        expected_output = "[BaseModel] ({}) {}".format(test_instance.id, test_instance.__dict__)
        self.assertEqual(str(test_instance), expected_output)


if __name__ == '__main__':
    unittest.main()
