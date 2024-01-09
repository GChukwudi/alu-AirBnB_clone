#!/usr/bin/python3
"""
Module for the BaseModel class.
"""
import uuid
from datetime import datetime


class BaseModel:
    """
    A base class for other models
    providing common attributes and methods.
    """
    def __init__(self):
        """
        Initialize a new instance of the BaseModel
        """
        self.id = str(uuid.uuid4()) 

        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """
        Update the 'updated_at' attribute with the current datetime
        """
        self.updated_at = datetime.now()

    def to_dict(self):
        """
        Returns a dictionary containing all keys/values of __dict__ of the instance
        """
        key_dict = self.__dict__.copy()
        key_dict["__class__"] = self.__class__.__name__
        key_dict["created_at"] = self.created_at.isoformat()
        key_dict["updated_at"] = self.updated_at.isoformat()

        return key_dict

    def __str__(self):
        """
        Return a string representation of the BaseModel
        """
        name = self.__class__.__name__
        return "[{}] ({}) {}".format (name, self.id, self.__dict__)


if __name__ == "__main__":
    my_model = BaseModel()
    my_model.name = "My First Model"
    my_model.my_number = 89
    print(my_model)
    my_model.save()
    print(my_model)
    my_model_json = my_model.to_dict()
    print(my_model_json)
    print("JSON of my_model:")
    for key in my_model_json.keys():
        print("\t{}: ({}) - {}".format(key, type(my_model_json[key]), my_model_json[key]))
