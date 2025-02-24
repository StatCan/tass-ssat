import unittest
from pathlib import Path
from tass.converter.conf import excel as excel
import json


class TestConvert(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("Beginning new test TestCase %s" % self._testMethodName)
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

    def test_Convert(self):
        flder = str(Path(__file__).parent.resolve())
        excel_path = (Path(flder)
                      .joinpath("data", "simple_demo")
                      .with_suffix(".xlsx"))
        excel_conf = excel.convert(excel_path)

        expected_path1 = (Path(flder)
                          .joinpath("data", "test--tr1")
                          .with_suffix(".json"))
        expected_path2 = (Path(flder)
                          .joinpath("data", "test--tr2")
                          .with_suffix(".json"))

        with open(file=expected_path1, mode='r') as f:
            expected_file1 = json.load(f)

        with open(file=expected_path2, mode='r') as f:
            expected_file2 = json.load(f)

        breakpoint()
        self.assertIn(expected_file1, excel_conf)
        self.assertIn(expected_file2, excel_conf)


if __name__ == '__main__':
    unittest.main()
