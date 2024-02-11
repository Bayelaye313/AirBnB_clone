#!/usr/bin/python3
"""Defines the FileStorage class."""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """Handles serialization and deserialization
    of instances to and from JSON.
    Attributes:
        __file_path (str): The name of the file to save objects to.
        __objects (dict): A dictionary of instantiated objects.
    """

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns a dictionary of all stored objects."""
        return self.__objects

    def new(self, obj):
        """Stores a new object."""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """Serializes objects to JSON and writes to file."""
        objects_dict = {
            key: val.to_dict()
            for key, val in self.__objects.items()
        }

        with open(self.__file_path, 'w') as file:
            json.dump(objects_dict, file)

    def reload(self):
        """Deserializes JSON file to objects."""
        try:
            with open(self.__file_path, 'r') as file:
                objects_dict = json.load(file)
                for obj_dict in objects_dict.values():
                    cls_name = obj_dict.pop("__class__", None)
                    if cls_name:
                        cls = globals().get(cls_name)
                        if cls:
                            self.new(cls(**obj_dict))
        except FileNotFoundError:
            pass
