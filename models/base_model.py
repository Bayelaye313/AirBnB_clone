#!/usr/bin/python3
"""This file contain the parent class BaseModel"""
import uuid
from datetime import datetime, date, time, timedelta

class BaseModel :
    """BaseModel class"""
    def __init__(self, *args, **kwargs):
        """
        __init__ constructor method of the class
        
        Attributes:
            args (list): inputted arguments as a list.
            kwargs (dict): inputted arguments as a dict.
            id (str) - assign with an uuid when an instance is created.
            created_at (time): datetime - assign with the current datetime when
                an instance is created.
            updated_at (time): datetime - assign with the current datetime when
                n instance is created and it will be updated every time you
                change your object.

        """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        
        def __str__(self):
            """Return the print/str representation of the BaseModel instance."""
            return "[{}] ({}) {}".format(self.__class__.name, self.id, self.__dict__)
        
        def save(self):
            """updates the public instance attribute updated_at with the current datetime"""
            self.updated_at = datetime.now()
            
        def to_dict(self):
            """returns a dictionary containing all keys/values of __dict__ of the instance"""
            obj_dict = self.__dict__copy()
            obj_dict['created_at'] = self.created_at.isoformat()
            obj_dict['updated_at'] = self.updates_at.isoformat()
            
    