#!/usr/bin/python3
"""Defines unittests for models/user.py.

Unittest classes:
    TestUser_instantiation
    TestUser_save
    TestUser_to_dict
"""
from models.base_model import BaseModel
from models import storage
import unittest
from models.user import User


class TestUserInstantiation(unittest.TestCase):
    def test_instantiation(self):
        user = User()
        self.assertTrue(isinstance(user, User))
        self.assertTrue(issubclass(User, BaseModel))
        self.assertEqual(user.email, "")
        self.assertEqual(user.password, "")
        self.assertEqual(user.first_name, "")
        self.assertEqual(user.last_name, "")


class TestUserSave(unittest.TestCase):
    def test_save(self):
        user = User()
        user.email = "test@example.com"
        user.password = "password123"
        user.first_name = "John"
        user.last_name = "Doe"
        user.save()
        key = "User." + user.id
        obj_dict = storage.all()["User"]
        self.assertTrue(key in obj_dict)
        self.assertEqual(obj_dict[key].to_dict(), user.to_dict())


class TestUserToDict(unittest.TestCase):
    def test_to_dict(self):
        user = User()
        user.email = "test@example.com"
        user.password = "password123"
        user.first_name = "John"
        user.last_name = "Doe"
        user_dict = user.to_dict()
        self.assertEqual(user_dict["email"], "test@example.com")
        self.assertEqual(user_dict["password"], "password123")
        self.assertEqual(user_dict["first_name"], "John")
        self.assertEqual(user_dict["last_name"], "Doe")
        self.assertEqual(user_dict["__class__"], "User")


if __name__ == "__main__":
    unittest.main()
