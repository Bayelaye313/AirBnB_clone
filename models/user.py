#!/usr/bin/python3
"""Defines the User class."""
import models
from models.base_model import BaseModel


class User(BaseModel):
    """Represent a User.

    Attributes:
        email (str): The email of the user.
        password (str): The password of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
    """
    @classmethod
    def all(cls):
        """Returns a dictionary of all instances of the class."""
        return {k: v for k, v in models.storage.all().items() if isinstance(v, cls)}

    email = ""
    password = ""
    first_name = ""
    last_name = ""
