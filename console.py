#!/usr/bin/python3
"""contains the entry point of the command interpreter"""
import cmd
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Defines the RBnB command interpreter.

    Attributes:
        prompt (str): The command prompt.
    """
    prompt = "(hbnb) "

    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def help_quit(self):
        """Help documentation for the quit command."""
        print("Quit command to exit the program")

    def do_EOF(self, arg):
        """Handle End-Of-File (EOF) to exit the program"""
        print("")  # Print a new line for better readability
        return True

    def help_EOF(self):
        """Help documentation for the EOF command."""
        print("Handle End-Of-File (EOF) to exit the program")

    def emptyline(self):
        """Called when an empty line is entered"""
        pass

    def do_create(self, args):
        """Creates a new instance of BaseModel, saves it (to the JSON file) and
        prints the id.
        """
        if(not args):
            print('** class name missing **')
        elif(args not in self.__classes):
            print("** class doesn't exist **")
        else:
            newModel = BaseModel()
            newModel.save()
            print(newModel.id)

    def help_create(self):
        """Help documentation for the create command."""
        print("Create a new instance of BaseModel. Usage: create <class name>")

    def do_show(self, arg):
        """Prints the string representation of an
        instance based on the class name and id
        """
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in self.__classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        obj_id = args[1]
        obj_store = storage.all()
        obj_key = "{}.{}".format(class_name, obj_id)
        if obj_key not in obj_store:
            print("** no instance found **")
            return
        print(obj_store[obj_key])

    def do_all(self, arg):
        """Prints all string representation of all instances based or
        not on the class name.
        """
        class_name = arg.split()[0] if arg else None
        if class_name and class_name not in self.__classes:
            print("** class doesn't exist **")
            return

        if class_name:
            # Use class_name.all() to retrieve all instances of the specified class
            instances = eval(class_name).all()
            print([str(instance) for instance in instances.values()])
        else:
            # If no class name is specified, print all instances of all classes
            all_instances = storage.all()
            print([str(value) for value in all_instances.values()])

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and
        id (save the change into the JSON file)
        """
        args = arg.split()
        if not args:
            print("** class name missing **")
            return

        class_name = args[0]
        if class_name not in self.__classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        obj_id = args[1]
        obj_store = storage.all()
        obj_key = "{}.{}".format(class_name, obj_id)

        if obj_key not in obj_store:
            print("** no instance found **")
        else:
            del obj_store[obj_key]
            storage.save()

    def do_update(self, arg):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
        <class>.update(<id>, <attribute_name>, <attribute_value>) or
        <class>.update(<id>, <dictionary>)
            Update a class instance of a given id by adding or updating
            a given attribute key/value pair or dictionary.
        """
        argl = arg.split()
        objdict = storage.all()

        if len(argl) == 0:
            print("** class name missing **")
            return False
        if argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(argl) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(argl[0], argl[1]) not in objdict.keys():
            print("** no instance found **")
            return False
        if len(argl) == 2:
            print("** attribute name missing **")
            return False
        if len(argl) == 3:
            try:
                type(eval(argl[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(argl) == 4:
            obj = objdict["{}.{}".format(argl[0], argl[1])]
            if argl[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[argl[2]])
                obj.__dict__[argl[2]] = valtype(argl[3])
            else:
                obj.__dict__[argl[2]] = argl[3]
        elif type(eval(argl[2])) == dict:
            obj = objdict["{}.{}".format(argl[0], argl[1])]
            for k, v in eval(argl[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
