#!/usr/bin/python3
"""
Module for the BaseModel class.
"""
import uuid
from datetime import datetime
import models


class BaseModel:
    """
    A base class for other models
    providing common attributes and methods.
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize a new instance of the BaseModel
        """
        time_format = "%Y-%m-%dT%H:%M:%S.%f"
        if kwargs:
            for key, value in kwargs.items():
                if key == "__class__":
                    continue

                if key in ['created_at', 'updated_at']:
                    value = datetime.strptime(value, time_format)

                setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()

        models.storage.new(self)

    def save(self):
        """
        Update the 'updated_at' attribute with the current datetime
        """
        self.updated_at = datetime.utcnow()
        models.storage.save()
        return self.updated_at

    def to_dict(self):
        """
        Returns a dictionary containing all keys
        And values of __dict__ of the instance
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
        return "[{}] ({}) {}".format(name, self.id, self.__dict__)


if __name__ == "__main__":
    my_model = BaseModel()
    my_model.name = "My_First_Model"
    my_model.my_number = 89
    print(my_model.id)
    print(my_model)
    print(type(my_model.created_at))
    print("--")
    my_model_json = my_model.to_dict()
    print(my_model_json)
    print("JSON of my_model:")
    for key in my_model_json.keys():
        print("\t{}: ({}) - {}".format(
            key,
            type(my_model_json[key]),
            my_model_json[key]
            ))
