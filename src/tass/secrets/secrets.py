import json
from pathlib import Path


class DataSource():

    def __init__(self, config_path):
        __path = Path(config_path).resolve()
        self._config_path = __path
        with open(__path) as conf:
            config = json.load(conf)
        self._load_datasource(config)

    def _load_datasource(self, config):
        raise NotImplementedError("Please implement this function.")

    def from_collection(self, collection):
        return self._collections[collection]
        
    
class Collection():
    def __init__(self, *args, **kwargs):
        self._entries = self._load_entries(*args, **kwargs)
        
    def _load_entries(self, *args, **kwargs):
        raise NotImplementedError("Please implement this function.")

    def select(self, where='key', comparison=None, value='', count=1):
        if where == 'key':
            return self._entries[value]
        else:

            def equals(actual, expected):
                return actual == expected

            matches = []
            match comparison:
                case 'equals' | 'e':
                    compare = equals 

            for key, entry in self._entries.items():
                if compare(entry.get(where), value):
                    if count == 1:
                        return entry
                    else:
                        matches.append(entry)



class Entry():
    def __init__(self, data):
        self._data = data

    def get(self, key):
        return self._data[key]