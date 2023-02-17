import unittest
import json
from jsonschema import Draft7Validator

class TestJsonSchema(unittest.TestCase):
    def setUp(self):
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("Beginning new test TestCase %s" % self._testMethodName)
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

        with open("templates/templates.json") as f:
            self.schema = json.load(f)

    def test_JsonSchemaValidate(self):
        print(self.schema)
        print("Schema validator result:")
        print(Draft7Validator.check_schema(self.schema))

if __name__ == '__main__':
    unittest.main()
