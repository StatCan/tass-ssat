import openpyxl
import tass.secrets.secrets as secrets
from pathlib import Path


class Excel(secrets.DataSource):

    def __init__(self, config):
        super.__init__(config)
    
    def _load_config(self, config_path):
        config = super()._load_config(config_path)
        source_path = Path(config['source']['path']).resolve()
        self._source = openpyxl.Workbook(source_path)
        
        
    def _load_collections(self, collections):
        for coll in collections:
            _name = coll['name']
            _entry_set = coll['entry-set']
            
        

    class Sheet(secrets.Collection):
        def __init__(self, collection, entry_set):
            super().__init__(collection=collection, entry_set=entry_set)
            

        def _load_entry_set(self, entry_set):
            self._columns = []
            self._name = entry_set['name']
            _key = entry_set['key']
            _cols = entry_set['columns']
            ColumnDefinition = namedtuple("ColumnDefinition", "name, column")
            for col in _cols:
                self._columns.append(ColumnDefinition(col['name'], col['column']))
            
            start_row = 2 if has_headers else 1
            _entries = {}
            for index, row in enumerate(collection.iter_rows(min_row=start_row), start_row):
                entry = {"row": index}
                for col in self._columns:
                    entry[col.name] = row[col.column]
                _entries[_key] = Excel.Row(entry)
            
            return _entries
            

    class Row(secrets.Entry):
        def __init__(self, data):
            super().__init__(data)