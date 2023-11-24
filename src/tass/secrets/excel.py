import openpyxl
import tass.secrets.secrets as secrets
from pathlib import Path
from collections import namedtuple


class Excel(secrets.DataSource):

    def __init__(self, config):
        super().__init__(config)
    

    def _load_datasource(self, config):
        _source_path = Path(config['source']['path']).resolve()
        _source = config['source']
        _all_collections = config['collections']

        _collections = [_c for _c in _all_collections if _c['name'] in _source['collections']] 


        self._collections = self._load_collections(
                                openpyxl.load_workbook(_source_path),
                                _collections, config['entry-sets'])
        
        
    def _load_collections(self, source, collections, entry_sets):
        _loaded = {}
        for coll in collections:
            _name = coll['name']
            _entry_set = [se for se in entry_sets if se['name'] == coll['entry-set']][0]
            _wsheet = source[_name]
            _loaded[_name] = Excel.Sheet(_wsheet, _entry_set)
        return _loaded
            
        

    class Sheet(secrets.Collection):
        def __init__(self, collection, entry_set):
            super().__init__(collection=collection, entry_set=entry_set)
            

        def _load_entries(self, collection, entry_set):
            breakpoint()
            self._columns = []
            self._name = collection.title
            _key = entry_set['key']
            _cols = entry_set['columns']
            _has_headers = entry_set['has-headers']
            ColumnDefinition = namedtuple("ColumnDefinition", "name, column")
            for col in _cols:
                self._columns.append(ColumnDefinition(col['name'], col['column']))
            
            start_row = 2 if _has_headers else 1
            _entries = {}
            for index, row in enumerate(collection.iter_rows(min_row=start_row), start_row):
                entry = {"row": index}
                for col in self._columns:
                    entry[col.name] = row[col.column].value
                _entries[entry[_key]] = Excel.Row(entry)
            
            return _entries
            

    class Row(secrets.Entry):
        def __init__(self, data):
            super().__init__(data)