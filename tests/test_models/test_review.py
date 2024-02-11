#!/usr/bin/python3
"""Defines unittests for models/review.py.

Unittest classes:
    TestReview_instantiation
    TestReview_save
    TestReview_to_dict
"""
import unittest
from models.review import Review
from models import storage


class TestReviewInstantiation(unittest.TestCase):
    def test_instantiation(self):
        review = Review()
        self.assertTrue(isinstance(review, Review))
        self.assertEqual(review.place_id, "")
        self.assertEqual(review.user_id, "")
        self.assertEqual(review.text, "")


class TestReviewSave(unittest.TestCase):
    def test_save(self):
        review = Review()
        review.place_id = "place_id_123"
        review.user_id = "user_id_456"
        review.text = "Great experience!"
        review.save()
        key = "Review." + review.id
        obj_dict = storage.all()["Review"]
        self.assertTrue(key in obj_dict)
        self.assertEqual(obj_dict[key].to_dict(), review.to_dict())


class TestReviewToDict(unittest.TestCase):
    def test_to_dict(self):
        review = Review()
        review.place_id = "place_id_123"
        review.user_id = "user_id_456"
        review.text = "Great experience!"
        review_dict = review.to_dict()
        self.assertEqual(review_dict["place_id"], "place_id_123")
        self.assertEqual(review_dict["user_id"], "user_id_456")
        self.assertEqual(review_dict["text"], "Great experience.")
        self.assertEqual(review_dict["__class__"], "Review")


if __name__ == "__main__":
    unittest.main()
