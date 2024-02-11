#!/usr/bin/python3
"""Defines the State class."""
import models
from models.base_model import BaseModel


class State(BaseModel):
    """Represent a state.

    Attributes:
        name (str): The name of the state.
    """
    @classmethod
    def all(cls):
        """Returns a dictionary of all instances of the class."""
        return {k: v for k, v in models.storage.all().items() if isinstance(v, cls)}

    name = ""
