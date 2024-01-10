#!/usr/bin/python3
"""
Module for console
"""
import cmd
import shlex
from models.base_model import BaseModel
from models import storage


class HBNBCommand(cmd.Cmd):
    """
    HBNBCommand console class
    """
    prompt = '(hbnb) '
    classes = ["BaseModel"]

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program"""
        print("")
        return True

    def emptyline(self):
        """
        Do nothing on an empty line
        """
        pass

    def do_create(self, arg):
        """
        Creates a new instance of BaseModel, saves it, and prints the id
        """
        command = shlex.split(arg)

        if len(command) == 0:
            print("** class name missing **")
        elif command[0] not in self.classes:
            print("** class doesn't exist **")
        else:
            new_instance = BaseModel()
            new_instance.save()
            print(new_instance.id)

    def do_show(self, arg):
        """
        Prints the string representation of an instance
        """
        command = shlex.split(arg)

        if len(command) == 0:
            print("** class name missing **")
        elif command[0] not in self.classes:
            print("** class doesn't exist **")
        elif len(command) < 2:
            print("** instance id missing **")
        else:
            objects = storage.all()

            key = "{}.{}".format(command[0], command[1])
            if key in objects:
               print(objects[key])
            else:
                print("** no instance found **")

    def do_destroy(self, arg):
        command = shlex.split(arg)

        if len(command) == 0:
            print("** class name missing **")
        elif command[0] not in self.classes:
            print("** class doesn't exist **")
        elif len(command) < 2:
            print("** instance id missing **")
        else:
            objects = storage.all()
            key = "{}.{}".format(command[0], command[1])
            if key in objects:
                del objects[key]
                storage.save()
            else:
                print("** no instance found **")

    def do_all(self, arg):
        objects = storage.all()

        command = shlex.split(arg)
        if len(command) == 0:
            for key, value in objects.items():
                print(str(value))
        elif command[0] not in self.classes:
            print("** class doesn't exist **")
        else:
            for key, value in objects.items():
                if key.split('.')[0] == command[0]:
                    print(str(value))

    def do_update(self, arg):
        """Updates an instance based on the class name and id."""
        command = shlex.split(arg)
        if len(command) == 0:
            print("** class name missing **")
        elif command[0] not in self.classes:
            print("** class doesn't exist **")
        elif len(command) < 2:
            print("** instance id missing **")
        else:
            objects = storage.all()

            key = "{}.{}".format(command[0], command[1])
            if key not in objects:
                print("** no instance found **")
            elif len(command) < 3:
                print("** attribute name missing **")
            elif len(command) < 4:
                print("** value missing **")
            else:
                obj = objects[key]
                attribute_name = command[2]
                attribute_value = command[3]

                # Check if the attribute name is valid
                if not hasattr(obj, attribute_name):
                    print("** invalid attribute name **")
                else:
                    # Perform type conversion based on attribute type
                    attribute_type = type(getattr(obj, attribute_name))
                    try:
                        attribute_value = attribute_type(attribute_value)
                    except (ValueError, TypeError):
                        print("** invalid value type **")
                        return

                    setattr(obj, attribute_name, attribute_value)
                    obj.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
