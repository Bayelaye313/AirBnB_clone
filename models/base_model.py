#!/usr/bin/python3
"""Defines the BaseModel class."""
import uuid
from datetime import datetime
import models


class BaseModel:
    """Represents a base model."""
    def __init__(self, *args, **kwargs):
        """
        Initializes a new BaseModel instance.

        Args:
            args (list): Inputted arguments as a list.
            kwargs (dict): Inputted arguments as a dict.
        """
        if kwargs:
            for key, val in kwargs.items():
                if key in ['updated_at', 'created_at']:
                    form = "%Y-%m-%dT%H:%M:%S.%f"
                    setattr(self, key, datetime.strptime(val, form))
                elif key != '__class__':
                    setattr(self, key, val)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        models.storage.new(self)

    def __str__(self):
        """Returns the string representation of the BaseModel instance."""
        return ("[{}] ({}) {}"
                .format(self.__class__.__name__, self.id, self.__dict__))

    def save(self):
        """Updates the public instance attribute updated_at
        with the current datetime.
        """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """Returns a dictionary containing all keys/values
        of __dict__ of the instance.
        """
        obj_dict = self.__dict__.copy()
        obj_dict['__class__'] = self.__class__.__name__
        obj_dict['created_at'] = self.created_at.isoformat()
        obj_dict['updated_at'] = self.updated_at.isoformat()
        return obj_dict
