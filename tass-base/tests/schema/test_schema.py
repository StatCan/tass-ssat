import unittest
import json
from pathlib import Path
from tass.base.schema import validate, parse
from tass.base.schema.parser import Tass1Parser
from jsonschema.exceptions import ValidationError
from tass.base.core.tass_files import TassRun


class TestSchema(unittest.TestCase):
    def setUp(self):
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("Beginning new test TestCase %s" % self._testMethodName)
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

    def test_validate(self):
        path = (Path(__file__)
                .parents[1]
                .joinpath("./data/simple_demo.json")
                .resolve())
        with open(path) as f:
            job = json.load(f)
        parser = validate.validate(job)

        self.assertTrue(isinstance(parser, Tass1Parser))

    def test_validateFail(self):
        job = {"testing": "This should fail"}
        with self.assertRaises(ValidationError):
            validate.validate(job)

    def test_parse(self):
        path = (Path(__file__)
                .parents[1]
                .joinpath("./data/simple_demo.json")
                .resolve())
        test, _ = parse.parse(path)
        self.assertIsInstance(test, list)
        self.assertEqual(len(test), 2)
        for t in test:
            self.assertIsInstance(t, TassRun)
