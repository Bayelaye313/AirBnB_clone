#!/usr/bin/python3
"""contains the entry point of the command interpreter"""
import cmd
import sys

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

    
    
    
if __name__ == '__main__':
    HBNBCommand().cmdloop()
    