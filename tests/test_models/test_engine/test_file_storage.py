#!/usr/bin/python3
"""Defines unittests for models/engine/file_storage.py.

Unittest classes:
    TestFileStorage_instantiation
    TestFileStorage_methods
"""
import os
import unittest
from models import storage
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.user import User
from models.state import State
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review


class TestFileStorage_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the FileStorage class."""

    def test_FileStorage_instantiation(self):
        self.assertIsInstance(storage, FileStorage)

    def test_storage_initializes(self):
        self.assertEqual(type(storage), FileStorage)


class TestFileStorage_methods(unittest.TestCase):
    """Unittests for testing methods of the FileStorage class."""

    @classmethod
    def setUpClass(cls):
        cls.file_path = "file.json"
        cls.objects = storage._FileStorage__objects.copy()

    @classmethod
    def tearDownClass(cls):
        storage._FileStorage__objects = cls.objects
        try:
            os.remove(cls.file_path)
        except FileNotFoundError:
            pass

    def test_all(self):
        self.assertIsInstance(storage.all(), dict)

    def test_new(self):
        bm = BaseModel()
        us = User()
        st = State()
        pl = Place()
        cy = City()
        am = Amenity()
        rv = Review()
        models = [bm, us, st, pl, cy, am, rv]
        for model in models:
            models.storage.new(model)
        for model in models:
            self.assertIn(model, models.storage.all().values())

    def test_save_reload(self):
        bm = BaseModel()
        us = User()
        st = State()
        pl = Place()
        cy = City()
        am = Amenity()
        rv = Review()
        models = [bm, us, st, pl, cy, am, rv]
        for model in models:
            models.storage.new(model)
        models.storage.save()
        storage.reload()
        for model in models:
            self.assertIn(model, models.storage.all().values())
    def test_save(self):
        """Test that save method updates the updated_at attribute."""
        model = BaseModel()
        old_updated_at = model.updated_at
        model.save()
        new_updated_at = model.updated_at
        self.assertNotEqual(old_updated_at, new_updated_at)    


if __name__ == "__main__":
    unittest.main()
