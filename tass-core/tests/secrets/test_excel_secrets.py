import unittest
import pathlib
from tass.core.tools.secrets import Secrets
from tass.core.tools.singleton import Singleton
import tass.core.secrets.excel as excel


class TestExcelSecrets(unittest.TestCase):
    def setUp(self):
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("Beginning new test TestCase %s" % self._testMethodName)
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

    def test_creation(self):
        self.assertFalse(Singleton.exists(Secrets))
        path = '/data/excel_secrets_demo.json'
        directory = str(pathlib.Path(__file__).parents[1].resolve())
        file = directory + path
        Secrets().add_source(file)

        self.assertTrue(Singleton.exists(Secrets))
        self.assertIsInstance(
            Secrets().get_data_source('excel-test'),
            excel.Excel)

    def test_sheets(self):
        path = '/data/excel_secrets_demo.json'
        directory = str(pathlib.Path(__file__).parents[1].resolve())
        file = directory + path
        Secrets().add_source(file)
        excel = Secrets().get_data_collection('excel-test', 'CollectionA')
        excel2 = Secrets().get_data_collection('excel-test', 'CollectionB')

        self.assertEqual(len(excel.columns), 2)
        self.assertEqual(len(excel2.columns), 3)

        self.assertEqual(len(excel.entries), 16)
        self.assertEqual(len(excel2.entries), 16)

    def test_entries(self):
        path = '/data/excel_secrets_demo.json'
        directory = str(pathlib.Path(__file__).parents[1].resolve())
        file = directory + path
        Secrets().add_source(file)
        excel = Secrets().get_data_collection('excel-test', 'CollectionB')

        self.assertTrue(all(map((lambda e: e.has('Test') and
                                e.has('Sample') and
                                e.has('Third')),
                            excel.entries.values())))
        self.assertTrue(all(map((lambda e: e[0] == e[1].get('Sample')),
                            excel.entries.items())))

    def test_select_key(self):
        path = '/data/excel_secrets_demo.json'
        directory = str(pathlib.Path(__file__).parents[1].resolve())
        file = directory + path
        Secrets().add_source(file)
        excel = Secrets().get_data_collection('excel-test', 'CollectionA')
        entry = excel.select(value='a')

        self.assertEqual(entry.get('Sample'), 1000)

    def test_select_equals(self):
        path = '/data/excel_secrets_demo.json'
        directory = str(pathlib.Path(__file__).parents[1].resolve())
        file = directory + path
        Secrets().add_source(file)
        excel = Secrets().get_data_collection('excel-test', 'CollectionB')

        entry = excel.select(where='Sample', comparison='e', value='c')
        entry2 = excel.select(where='Third', comparison='e',
                              value='X', count=4)

        self.assertEqual(entry.get('Test'), 1002)
        self.assertEqual(len(entry2), 4)
        self.assertTrue(all(map((lambda e: e.get('Third') == 'X'), entry2)))

    def tearDown(self):
        Singleton.reset(Secrets)
