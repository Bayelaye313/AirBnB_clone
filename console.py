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

    class_dict = {"BaseModel": BaseModel, "User": User, "State": State,
               "City": City, "Amenity": Amenity, "Place": Place,
               "Review": Review}

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
        """Creates a new instance of a class, saves it to the JSON file,
        and prints the id."""
        if not args:
            print('** class name missing **')
        elif args not in self.class_dict:
            print("** class doesn't exist **")
        else:
            new_instance = self.class_dict[args]()  # Instantiate the class
            new_instance.save()  # Save the instance
            print(new_instance.id)  # Print the instance id

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
        if class_name not in self.class_dict:
            print("** class doesn't exist **")
            return
        if len(args) == 1:
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
            'Show all instances based on class name.'
            my_arg = arg.split(" ")
            if not arg:
                my_list = []
                my_objects = storage.all()
                for key, values in my_objects.items():
                    my_list.append(str(values))
                print(my_list)
            elif my_arg[0] not in self.class_dict:
                print("** class doesn't exist **")
            else:
                my_list = []
                my_objects = storage.all(self)
                for key, values in my_objects.items():
                    my_key = key.split(".")
                    if my_key[0] == my_arg[0]:
                        my_list.append(str(values))
                print(my_list)

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and
        id (save the change into the JSON file)
        """
        args = arg.split()
        if not args:
            print("** class name missing **")
            return

        class_name = args[0]
        if class_name not in self.class_dict:
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
        if argl[0] not in HBNBCommand.class_dict:
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

    def do_count(self, arg):
        'Count all instances based on class name.'
        count = 0
        my_arg = arg.split(" ")
        if not arg:
            # Si aucun argument n'est fourni, affichez le nombre total d'instances
            my_objects = storage.all()
            for key, values in my_objects.items():
                count += 1
            print(count)
        elif len(my_arg) == 1:
            # Si un seul argument est fourni, vérifiez si la classe existe et affichez le nombre d'instances
            if my_arg[0] not in self.class_dict:
                print("** class doesn't exist **")
                return
            my_objects = storage.all()
            for key, values in my_objects.items():
                my_key = key.split(".")
                if my_key[0] == my_arg[0]:
                    count += 1
            print(count)
        else:
            # Si plus d'un argument est fourni, affichez un message d'erreur
            print("Too many arguments")

    def do_command(self, class_name, method, arg):
        """Handle a command for a given class."""
        the_class = class_name.capitalize()
        my_arg = arg.split(".")
        if my_arg[1] == 'all()':
            method(arg)  # Here we only need to pass the argument 'all', the_class is not required
        elif my_arg[1] == 'count()':
            method(arg)  # Similarly, here we only need to pass the argument 'count', the_class is not required
        else:
            prim = my_arg[1].find('("')
            seco = my_arg[1].find('")')
            my_arg1 = my_arg[1][0:prim]
            my_arg2 = my_arg[1][prim + 2: seco]
            if my_arg1 == "show":
                param = f"{the_class} {my_arg2}"
                self.do_show(param)  # Use self instead of HBNBCommand
            elif my_arg1 == "destroy":
                param = f"{the_class} {my_arg2}"
                self.do_destroy(param)  # Use self instead of HBNBCommand
            else:
                my_arg3 = arg.replace('"', ' ').split(',')
                if len(my_arg3) == 0:
                    print("** instance id missing **")
                elif len(my_arg3) == 1:
                    print("** attribute name missing **")
                elif len(my_arg3) == 2:
                    print("** value missing **")
                else:
                    param = f"{the_class} {my_arg3[0][9:]} {my_arg3[1]} {my_arg3[2][1:-1]}"
                    self.do_update(param)

    def do_BaseModel(self, arg):
        """Handle commands for BaseModel."""
        if arg == "":
            print("** missing action **")
        else:
            self.do_command("BaseModel", self.do_all, arg)

    def do_User(self, arg):
        """Handle commands for User."""
        self.do_command("User", self.do_all, arg)

    def do_State(self, arg):
        """Handle commands for State."""
        self.do_command("State", self.do_all, arg)

    def do_City(self, arg):
        """Handle commands for City."""
        self.do_command("City", self.do_all, arg)

    def do_Amenity(self, arg):
        """Handle commands for Amenity."""
        self.do_command("Amenity", self.do_all, arg)

    def do_Place(self, arg):
        """Handle commands for Place."""
        self.do_command("Place", self.do_all, arg)

    def do_Review(self, arg):
        """Handle commands for Review."""
        self.do_command("Review", self.do_all, arg)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
