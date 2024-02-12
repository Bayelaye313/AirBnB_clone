#!/usr/bin/python3
"""Defines unittests for console.py.

Unittest classes:
    TestHBNBCommand_prompting
    TestHBNBCommand_help
    TestHBNBCommand_exit
    TestHBNBCommand_create
    TestHBNBCommand_show
    TestHBNBCommand_all
    TestHBNBCommand_destroy
    TestHBNBCommand_update
"""
import os
import sys
import unittest
from models import storage
from models.engine.file_storage import FileStorage
from console import HBNBCommand
from io import StringIO
from unittest.mock import patch


class TestHBNBCommand_prompting(unittest.TestCase):
    """Unittests for testing prompting of the HBNB command interpreter."""

    def setUp(self):
        self.command = HBNBCommand()

    def test_prompt_string(self):
        self.assertEqual("(hbnb) ", HBNBCommand.prompt)

    def test_empty_line(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(self.command.onecmd(""))
            self.assertEqual("", output.getvalue().strip())


class TestHBNBCommand_help(unittest.TestCase):
    """Unittests for testing help messages of the HBNB command interpreter."""

    def test_help_quit(self):
        h = "Quit command to exit the program."
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help quit"))
            self.assertEqual(h, output.getvalue().strip())

    def test_help_create(self):
        h = ("Usage: create <class>\n        "
             "Create a new class instance and print its id.")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help create"))
            self.assertEqual(h, output.getvalue().strip())

    def test_help_EOF(self):
        h = "EOF signal to exit the program."
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help EOF"))
            self.assertEqual(h, output.getvalue().strip())


class TestHBNBCommand_exit(unittest.TestCase):
    """Unittests for testing exiting from the HBNB command interpreter."""

    def test_quit_exits(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertTrue(HBNBCommand().onecmd("quit"))

    def test_EOF_exits(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertTrue(HBNBCommand().onecmd("EOF"))


class TestHBNBCommand_create(unittest.TestCase):
    """Unittests for testing create from the HBNB command interpreter."""

    @classmethod
    def setUpClass(cls):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def helper_test_create_object(self, class_name):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(f"create {class_name}"))
            obj_id = output.getvalue().strip()
            self.assertLess(0, len(obj_id))
            test_key = f"{class_name}.{obj_id}"
            self.assertIn(test_key, storage.all().keys())

    def test_create_missing_class(self):
        correct = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create"))
            self.assertEqual(correct, output.getvalue().strip())

    def test_create_invalid_class(self):
        correct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create MyModel"))
            self.assertEqual(correct, output.getvalue().strip())

    def test_create_invalid_syntax(self):
        correct = "*** Unknown syntax: MyModel.create()"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("MyModel.create()"))
            self.assertEqual(correct, output.getvalue().strip())
        correct = "*** Unknown syntax: BaseModel.create()"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.create()"))
            self.assertEqual(correct, output.getvalue().strip())

    def test_create_object(self):
        classes_to_test = ["BaseModel", "User", "State", "City",
                           "Amenity", "Place", "Review"]
        for class_name in classes_to_test:
            self.helper_test_create_object(class_name)


class TestHBNBCommand_show(unittest.TestCase):
    """Unittests for testing show from the HBNB command interpreter"""

    @classmethod
    def setUpClass(cls):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def helper_test_show(self, class_name, id, command):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(command))
            if id:
                obj = storage.all()[f"{class_name}.{id}"]
                self.assertEqual(obj.__str__(), output.getvalue().strip())
            else:
                correct = "** instance id missing **"
                self.assertEqual(correct, output.getvalue().strip())

    def test_show_missing_class(self):
        correct = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(".show()"))
            self.assertEqual(correct, output.getvalue().strip())

    def test_show_invalid_class(self):
        correct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show MyModel"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("MyModel.show()"))
            self.assertEqual(correct, output.getvalue().strip())

    def test_show_missing_id_space_notation(self):
        self.helper_test_show("BaseModel", None, "show BaseModel")
        self.helper_test_show("User", None, "show User")
        self.helper_test_show("State", None, "show State")
        self.helper_test_show("City", None, "show City")
        self.helper_test_show("Amenity", None, "show Amenity")
        self.helper_test_show("Place", None, "show Place")
        self.helper_test_show("Review", None, "show Review")

    def test_show_missing_id_dot_notation(self):
        self.helper_test_show("BaseModel", None, "BaseModel.show()")
        self.helper_test_show("User", None, "User.show()")
        self.helper_test_show("State", None, "State.show()")
        self.helper_test_show("City", None, "City.show()")
        self.helper_test_show("Amenity", None, "Amenity.show()")
        self.helper_test_show("Place", None, "Place.show()")
        self.helper_test_show("Review", None, "Review.show()")

    def test_show_no_instance_found_space_notation(self):
        # Créez un objet BaseModel pour chaque test
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            test_id = output.getvalue().strip()

        # Vérifiez que l'objet a été créé avec succès
        self.assertIn("BaseModel.{}".format(test_id), FileStorage.__objects.keys())
        # Testez l'affichage de l'objet nouvellement créé
        self.helper_test_show("BaseModel", "1", "show BaseModel 1")
        self.helper_test_show("User", "1", "show User 1")
        self.helper_test_show("State", "1", "show State 1")
        self.helper_test_show("City", "1", "show City 1")
        self.helper_test_show("Amenity", "1", "show Amenity 1")
        self.helper_test_show("Place", "1", "show Place 1")
        self.helper_test_show("Review", "1", "show Review 1")

    def test_show_no_instance_found_dot_notation(self):
        self.helper_test_show("BaseModel", "1", "BaseModel.show(1)")
        self.helper_test_show("User", "1", "User.show(1)")
        self.helper_test_show("State", "1", "State.show(1)")
        self.helper_test_show("City", "1", "City.show(1)")
        self.helper_test_show("Amenity", "1", "Amenity.show(1)")
        self.helper_test_show("Place", "1", "Place.show(1)")
        self.helper_test_show("Review", "1", "Review.show(1)")

    def test_show_objects_space_notation(self):
        classes_to_test = ["BaseModel", "User", "State", "City",
                           "Amenity", "Place", "Review"]
        for class_name in classes_to_test:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd(f"create {class_name}"))
                test_id = output.getvalue().strip()
            command = f"show {class_name} {test_id}"
            self.helper_test_show(class_name, test_id, command)

    def test_show_objects_dot_notation(self):
        classes_to_test = ["BaseModel", "User", "State", "City",
                           "Amenity", "Place", "Review"]
        for class_name in classes_to_test:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd(f"create {class_name}"))
                test_id = output.getvalue().strip()
            command = f"{class_name}.show({test_id})"
            self.helper_test_show(class_name, test_id, command)


class TestHBNBCommand_destroy(unittest.TestCase):
    """Unittests for testing destroy from the HBNB command interpreter."""

    @classmethod
    def setUpClass(cls):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        storage.reload()

    def setUp(self):
        self.command = HBNBCommand()

    def test_destroy_missing_class(self):
        test_cases = [
            {"cmd": "destroy",
             "expected_output": "** class name missing **"},
            {"cmd": ".destroy()",
             "expected_output": "** class name missing **"}
        ]
        self.run_test_cases(test_cases)

    def test_destroy_invalid_class(self):
        test_cases = [
            {"cmd": "destroy MyModel",
             "expected_output": "** class doesn't exist **"},
            {"cmd": "MyModel.destroy()",
             "expected_output": "** class doesn't exist **"}
        ]
        self.run_test_cases(test_cases)

    def test_destroy_id_missing_notation(self):
        test_cases = [
            {"cmd": "destroy BaseModel",
             "expected_output": "** instance id missing **"},
            {"cmd": "BaseModel.destroy()",
             "expected_output": "** instance id missing **"}
        ]
        self.run_test_cases(test_cases)

    def test_destroy_invalid_id(self):
        test_cases = [
            {"cmd": "destroy BaseModel 1",
             "expected_output": "** no instance found **"},
            {"cmd": "BaseModel.destroy(1)",
             "expected_output": "** no instance found **"}
        ]
        self.run_test_cases(test_cases)

    def test_destroy_objects(self):
        test_cases = [
            {"cmd": "create BaseModel", "expected_output": ""},
            {"cmd": "create User", "expected_output": ""},
            {"cmd": "create State", "expected_output": ""},
            {"cmd": "create Place", "expected_output": ""},
            {"cmd": "create City", "expected_output": ""},
            {"cmd": "create Amenity", "expected_output": ""},
            {"cmd": "create Review", "expected_output": ""}
        ]
        for test_case in test_cases:
            with self.subTest(test_case=test_case):
                with patch("sys.stdout", new=StringIO()) as output:
                    self.command.onecmd(test_case["cmd"])
                    test_id = output.getvalue().strip()
                obj_type = test_case["cmd"].split()[1]
                obj_key = "{}.{}".format(obj_type, test_id)
                destroy_cmd = "destroy {}".format(test_case["cmd"][7:])
                with patch("sys.stdout", new=StringIO()) as output:
                    self.command.onecmd(destroy_cmd)
                    self.assertNotIn(obj_key, storage.all())
                    self.assertNotIn(test_id, storage.all().keys())
                    self.assertEqual(test_case["expected_output"],
                                     output.getvalue().strip())

    def run_test_cases(self, test_cases):
        for test_case in test_cases:
            with self.subTest(test_case=test_case):
                with patch("sys.stdout", new=StringIO()) as output:
                    self.assertFalse(self.command.onecmd(test_case["cmd"]))
                    self.assertEqual(test_case["expected_output"],
                                     output.getvalue().strip())


class TestHBNBCommand_all(unittest.TestCase):
    """Unittests for testing all of the HBNB command interpreter."""

    @classmethod
    def setUpClass(cls):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def setUp(self):
        self.command = HBNBCommand()

    def test_all_invalid_class(self):
        test_cases = [
            {"cmd": "all MyModel",
             "expected_output": "** class doesn't exist **"},
            {"cmd": "MyModel.all()",
             "expected_output": "** class doesn't exist **"}
        ]
        self.run_test_cases(test_cases)

    def test_all_objects(self):
        test_cases = [
            {"cmd": "create BaseModel"},
            {"cmd": "create User"},
            {"cmd": "create State"},
            {"cmd": "create Place"},
            {"cmd": "create City"},
            {"cmd": "create Amenity"},
            {"cmd": "create Review"}
        ]
        for test_case in test_cases:
            with self.subTest(test_case=test_case):
                self.command.onecmd(test_case["cmd"])
        with patch("sys.stdout", new=StringIO()) as output:
            self.command.onecmd("all")
            for test_case in test_cases:
                self.assertIn(test_case["cmd"].split()[1],
                              output.getvalue().strip())

    def test_all_single_object(self):
        test_cases = [
            {"class": "BaseModel"},
            {"class": "User"},
            {"class": "State"},
            {"class": "Place"},
            {"class": "City"},
            {"class": "Amenity"},
            {"class": "Review"}
        ]
        for test_case in test_cases:
            with self.subTest(test_case=test_case):
                cmd = "create {}".format(test_case["class"])
                self.command.onecmd(cmd)
                with patch("sys.stdout", new=StringIO()) as output:
                    self.command.onecmd("all {}".format(test_case["class"]))
                    self.assertIn(test_case["class"],
                                  output.getvalue().strip())
                    obj_id = output.getvalue().strip().split()[0]
                    self.assertIn(obj_id, storage.all().keys())

    def run_test_cases(self, test_cases):
        for test_case in test_cases:
            with self.subTest(test_case=test_case):
                with patch("sys.stdout", new=StringIO()) as output:
                    self.assertFalse(self.command.onecmd(test_case["cmd"]))
                    self.assertEqual(test_case["expected_output"],
                                     output.getvalue().strip())


class TestHBNBCommand_update(unittest.TestCase):
    """Unittests for testing update from the HBNB command interpreter."""

    @classmethod
    def setUpClass(cls):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def setUp(self):
        self.command = HBNBCommand()

    def test_update_missing_class(self):
        test_cases = [
            {"cmd": "update",
             "expected_output": "** class name missing **"},
            {"cmd": ".update()",
             "expected_output": "** class name missing **"},
            {"cmd": "update MyModel",
             "expected_output": "** class doesn't exist **"},
            {"cmd": "MyModel.update()",
             "expected_output": "** class doesn't exist **"}
        ]
        self.run_test_cases(test_cases)

    def test_update_missing_id(self):
        test_cases = [
            {"cmd": "update BaseModel",
             "expected_output": "** instance id missing **"},
            {"cmd": "BaseModel.update()",
             "expected_output": "** instance id missing **"}
        ]
        self.run_test_cases(test_cases)

    def test_update_missing_attribute_name(self):
        test_cases = [
            {"cmd": "update BaseModel 1234",
             "expected_output": "** attribute name missing **"},
            {"cmd": "BaseModel.update(1234)",
             "expected_output": "** attribute name missing **"}
        ]
        self.run_test_cases(test_cases)

    def test_update_missing_value(self):
        test_cases = [
            {"cmd": 'update BaseModel 1234 name',
             "expected_output": "** value missing **"},
            {"cmd": 'BaseModel.update(1234, name)',
             "expected_output": "** value missing **"}
        ]
        self.run_test_cases(test_cases)

    def test_update_invalid_id(self):
        test_cases = [
            {"cmd": 'update BaseModel 1234 name "value"',
             "expected_output": "** no instance found **"},
            {"cmd": 'BaseModel.update(1234, name, "value")",',
             "expected_output": "** no instance found **"}
        ]
        self.run_test_cases(test_cases)

    def test_update_valid_input(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.command.onecmd("create BaseModel")
            test_id = output.getvalue().strip()
            self.assertIn("BaseModel.{}".format(test_id),
                          FileStorage.__objects.keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.command.onecmd("update BaseModel {} "
                                "name \"value\"".format(test_id))
            self.assertEqual("", output.getvalue().strip())
        obj = FileStorage.__objects["BaseModel.{}".format(test_id)]
        self.assertEqual("value", obj.name)

    def run_test_cases(self, test_cases):
        for test_case in test_cases:
            with self.subTest(test_case=test_case):
                with patch("sys.stdout", new=StringIO()) as output:
                    self.assertFalse(self.command.onecmd(test_case["cmd"]))
                    self.assertEqual(test_case["expected_output"],
                                     output.getvalue().strip())


if __name__ == "__main__":
    unittest.main()
