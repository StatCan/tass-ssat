import unittest
from tass.tools import conf
import json


class TestConvert(unittest.TestCase):
    def setUp(self):
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("Beginning new test TestCase %s" % self._testMethodName)
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

    def test_Convert(self):
        conf_file = conf.convert('tests/data/simple_demo.xlsx')
        conf_file = json.dumps(conf_file, indent=4)

        with open(file='tests/data/simple_demo.json', mode='r') as f:
            conf_file2 = json.load(f)

        with open(file='tests/data/testfile2.json', mode='w') as f:
            f.write(conf_file)

        with open(file='tests/data/testfile2.json', mode='r') as f:
            conf_file3 = json.load(f)

        self.assertEqual(conf_file2, conf_file3)


if __name__ == '__main__':
    unittest.main()
