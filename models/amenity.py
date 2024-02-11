#!/usr/bin/python3
"""Defines the Amenity class."""
import models
from models.base_model import BaseModel


class Amenity(BaseModel):
    """Represent an amenity.

    Attributes:
        name (str): The name of the amenity.
    """
    @classmethod
    def all(cls):
        """Returns a dictionary of all instances of the class."""
        return {k: v for k, v in models.storage.all().items() if isinstance(v, cls)}

    name = ""
