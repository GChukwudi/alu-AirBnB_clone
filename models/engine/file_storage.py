#!/usr/bin/python3
"""
"""
import os.path
import json
from models.base_model import BaseModel


class FileStorage:
    """
    """
    __file_path = "file.json"
    __objects = {}

    def new(self, obj):
        """
        """
        obj_name = obj.__class__.__name__
        key = "{}.{}".format(obj_name, obj.id)
        FileStorage.__objects [key] = obj

    def all(self):
        """
        """
        return FileStorage.__objects

    def save(self):
        """
        """
        all_objs = FileStorage.__objects
        obj_dict = {}

        for obj in all_objs.keys():
            obj_dict[obj] = all_objs[obj].to_dict()

        with open(FileStorage.__file_path, "w", encoding="utf-8") as file:
            json.dump(obj_dict, file)

    def reload(self):
        """
        """
        if os.path.isfile(FileStorage.__file_path):
            with open(FileStorage.__file_path, "r", encoding="utf-8") as file:
                try:
                    obj_dict = json.load(file)
                    for key, value in obj_dict.items():
                        name, obj_id = key.split('.')

                        cls = eval(name)
                        instance = cls(**value)

                        FileStorage.__objects[key] = instance
                except Exception:
                    raise TypeError 
