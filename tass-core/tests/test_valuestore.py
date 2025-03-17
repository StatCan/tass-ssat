import unittest
from tass.core.tools.valuestore import ValueStore
from tass.core.tools.singleton import Singleton


class TestValueStore(unittest.TestCase):
    def setUp(self):
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("Beginning new test TestCase %s" % self._testMethodName)
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

    def tearDown(self):
        Singleton.reset(ValueStore)

    def test_create(self):
        self.assertFalse(Singleton.exists(ValueStore),
                         msg="ValueStore should not be initialized.")
        ValueStore()
        self.assertTrue(Singleton.exists(ValueStore),
                        msg="ValueStore should be initialized.")

    def test_double_create(self):
        my_values = ValueStore()
        my_values2 = ValueStore()

        self.assertEqual(my_values, my_values2)

    def test_empty(self):
        my_values = ValueStore()
        self.assertTrue(my_values.is_empty())
        my_values.add_to_dict("key1", "test")
        self.assertFalse(my_values.is_empty())

    def test_add(self):
        my_values = ValueStore()
        self.assertEqual(len(my_values.value_dict.keys()), 0)
        my_values.add_to_dict("key1", "test string")
        self.assertEqual(len(my_values.value_dict.keys()), 1)
        self.assertEqual(my_values.get_data("key1"), "test string")

    def test_exists(self):
        my_values = ValueStore()
        self.assertFalse(my_values.contains("key1"))
        my_values.add_to_dict("key1", "test")
        self.assertTrue(my_values.contains("key1"))

    def test_add_double_create(self):
        my_values = ValueStore()
        my_values2 = ValueStore()
        my_values.add_to_dict("key1", "test")
        self.assertEqual(my_values2.get_data("key1"), "test")
        my_values3 = ValueStore()
        self.assertEqual(my_values3.get_data("key1"), "test")
        my_values3.add_to_dict("key2", "more test")
        self.assertEqual(my_values.get_data("key2"), "more test")


if __name__ == '__main__':
    unittest.main()
