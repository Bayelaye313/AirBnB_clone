#!/usr/bin/python3
"""Defines the Review class."""
import models
from models.base_model import BaseModel


class Review(BaseModel):
    """Represent a review.

    Attributes:
        place_id (str): The Place id.
        user_id (str): The User id.
        text (str): The text of the review.
    """
    @classmethod
    def all(cls):
        """Returns a dictionary of all instances of the class."""
        return {k: v for k, v in models.storage.all().items() if isinstance(v, cls)}

    place_id = ""
    user_id = ""
    text = ""
