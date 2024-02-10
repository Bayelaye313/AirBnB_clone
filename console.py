#!/usr/bin/python3
"""contains the entry point of the command interpreter"""
import cmd
from models import storage
from models.base_model import BaseModel


class HBNBCommand(cmd.Cmd):
    """Defines the RBnB command interpreter.

    Attributes:
        prompt (str): The command prompt.
    """
    prompt = "(hbnb)"
    
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
        """Creates a new instance of BaseModel, saves it (to the JSON file) and prints the id."""
        if(not args):
            print('** class name missing **')
        elif(args not in ["BaseModel"]):
            print("** class doesn't exist **")
        else:
            newModel = BaseModel()
            newModel.save()
            print(newModel.id)
    def help_create(self):
        """Help documentation for the create command."""
        print("Creates a new instance of BaseModel. Usage: create <class name>")
    def do_show(self, arg):
        """Prints the string representation of an instance based on the class name and id"""
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in ['BaseModel']:
            print("** class doesn't exist **")
            return
        if len(args) < 2 :
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
        """Prints all string representation of all instances based or not on the class name."""
        class_name = arg.split()[0] if arg else None
        if class_name and class_name not in ['BaseModel']:
            print("** class doesn't exist **")
            return
        obj_store = storage.all()
        
        if class_name:
            obj_store = {key: value for key, value in obj_store.items() if key.split('.')[0] == class_name}
        print([str(value) for value in obj_store.values()])
    
    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id (save the change into the JSON file)"""
        args = arg.split()
        class_name = args[0]
        class_id = arg[1]
        if not class_name:
            print("** class name missing **")
            return
        if class_name and class_name not in ["BaseModel"]:
            print("** class doesn't exist **")
            return
        if not class_id :
            print("** instance id missing **")
            return
if __name__ == '__main__':
    HBNBCommand().cmdloop()
    