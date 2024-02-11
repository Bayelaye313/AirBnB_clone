#!/usr/bin/python3
"""Defines the City class."""
import models
from models.base_model import BaseModel


class City(BaseModel):
    """Represent a city.

    Attributes:
        state_id (str): The state id.
        name (str): The name of the city.
    """
    @classmethod
    def all(cls):
        """Returns a dictionary of all instances of the class."""
        return {k: v for k, v in models.storage.all().items() if isinstance(v, cls)}

    state_id = ""
    name = ""
