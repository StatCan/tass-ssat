from .singleton import Singleton
import json
from pathlib import Path
from tass.secrets.excel import Excel


def _secret_type(secret_type):
    match secret_type:
        case 'excel':
            return Excel

class Secrets(metaclass=Singleton):
    def __init__(self):
        self._data_sources = {}

    def add_source(self, config_path):
        path = Path(config_path).resolve()
        with open(path) as conf:
            config = json.load(conf)

        key = config['source']['name']
        if self.contains(key):
            return

        source = _secret_type(config['source']['type'])(path, config)

        self._data_sources[key] = source

    def get_data_source(self, source):
        return self._data_sources[source]

    def get_data_collection(self, source, collection):
        return self.get_data_source(source)\
            .from_collection(collection)

    def get_data_entry(self, source, collection, **selection):
        return self.get_data_collection(source, collection).select(**selection)

    def contains(self, key):
        return key in self._data_sources

    def is_empty(self):
        if not bool(self._data_sources):
            return True
        return False
