#!/usr/bin/python3
"""
Module for FilStorage unittest
"""
import unittest
import os
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class TestFileStorage_instantiation(unittest.TestCase):
    """
    Unittests for testing instantiation of the FileStorage class.
    """

    def test_FileStorage_instantiation_no_args(self):
        self.assertEqual(type(FileStorage()), FileStorage)

    def test_FileStorage_instantiation_with_arg(self):
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_storage_initializes(self):
        self.assertEqual(type(models.storage), FileStorage)

class TestFileStorage(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_file.json"

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_all_storage_returns_dictionary(self):
        self.assertEqual(dict, type(models.storage.all()))

    def test_new(self):
        obj = BaseModel()
        models.storage.new(obj)
        self.assertIn("BaseModel.{}", format(obj.id), models.storage.all())

    def test_new_with_args(self):
        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), 1)

    def est_new_with_None(self):
        with self.assertRaises(AttributeError):
            models.storage.new(None)

    def test_save_reload(self):
        obj1 = BaseModel()
        obj2 = BaseModel()
        models.storage.new(obj1)
        models.storage.new(obj2)
        models.storage.save()

        new_storage = FileStorage()
        new_storage.reload()

        key1 = "{}.{}".format(obj1.__class__.__name__, obj1.id)
        key2 = "{}.{}".format(obj2.__class__.__name__, obj2.id)

        # Asserting that the objects were successfully reloaded
        self.assertTrue(key1 in new_storage.all())
        self.assertTrue(key2 in new_storage.all())

        # Asserting that the reloaded objects match the original objects
        self.assertEqual(new_storage.all()[key1].to_dict(), obj1.to_dict())
        self.assertEqual(new_storage.all()[key2].to_dict(), obj2.to_dict())

    def test_save_to_file(self):
        obj = Basemodel()
        models.storage.new(obj)
        models.storage.save()
        self.assertTrue(os.path.exists(models.storage._FileStorage__file_path))

    def test_reload_empty_file(self):
        with self.assertRaises(TypeError):
            models.storage.reload()

if __name__ == "__main__":
    unittest.main()
