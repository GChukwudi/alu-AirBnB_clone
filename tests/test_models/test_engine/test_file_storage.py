#!/usr/bin/python3
"""
Module for FileStorage unittest
"""
import unittest
import os
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class TestFileStorageInstantiation(unittest.TestCase):
    """
    Unittests for testing instantiation of the FileStorage class.
    """

    def test_FileStorage_instantiation_no_args(self):
        self.assertEqual(type(FileStorage()), FileStorage)

    def test_FileStorage_instantiation_with_arg(self):
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_storage_initializes(self):
        storage_instance = FileStorage()
        self.assertEqual(type(storage_instance), FileStorage)

class TestFileStorage(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_file.json"
        self.storage_instance = FileStorage()

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_objects(self):
        obj = BaseModel()
        self.storage_instance.new(obj)

        expected_key = "BaseModel.{}".format(obj.id)
        all_objects = self.storage_instance.all()
        if expected_key in all_objects:
            print("OK")
        else:
            print("Test failed. Expected key not found in __objects.")

    def test_save_creates_file(self):
        obj = BaseModel()
        self.storage_instance.new(obj)
        self.storage_instance.save()

        self.assertTrue(os.path.exists(self.storage_instance._FileStorage__file_path))

    def test_all_storage_returns_dictionary(self):
        self.assertEqual(dict, type(self.storage_instance.all()))

    def test_new(self):
        obj = BaseModel()
        self.storage_instance.new(obj)
        self.assertIn("BaseModel.{}".format(obj.id), self.storage_instance.all())

    def test_new_with_args(self):
        with self.assertRaises(TypeError):
            self.storage_instance.new(BaseModel(), 1)

    def test_new_with_None(self):
        with self.assertRaises(AttributeError):
            self.storage_instance.new(None)

    def test_save_reload(self):
        obj1 = BaseModel()
        obj2 = BaseModel()
        self.storage_instance.new(obj1)
        self.storage_instance.new(obj2)
        self.storage_instance.save()

        new_storage = FileStorage()
        new_storage.reload()

        self.assertTrue(new_storage.all().get("BaseModel.{}".format(obj1.id)) is not None)
        self.assertTrue(new_storage.all().get("BaseModel.{}".format(obj2.id)) is not None)

    def test_save_to_file(self):
        obj = BaseModel()
        self.storage_instance.new(obj)
        self.storage_instance.save()
        self.assertTrue(os.path.exists(self.storage_instance._FileStorage__file_path))

    def test_reload_empty_file(self):
        with self.assertRaises(TypeError):
            self.storage_instance.reload(None)

    def test_save_modifies_file(self):
        obj = BaseModel()
        self.storage_instance.new(obj)
        self.storage_instance.save()

        initial_mtime = os.path.getmtime(self.storage_instance._FileStorage__file_path)

        obj2 = BaseModel()
        self.storage_instance.new(obj2)
        self.storage_instance.save()

        current_mtime = os.path.getmtime(self.storage_instance._FileStorage__file_path)
        self.assertNotEqual(initial_mtime, current_mtime)

    def test_reload(self):
        obj = BaseModel()
        self.storage_instance.new(obj)
        self.storage_instance.save()

        new_storage = FileStorage()
        new_storage.reload()

        expected_key = "BaseModel.{}".format(obj.id)
        self.assertIn(expected_key, new_storage.all())

if __name__ == "__main__":
    unittest.main()
