from .singleton import Singleton
import json
from pathlib import Path
from ..log.logging import getLogger
from ..secrets.excel import Excel


log = getLogger(__name__)


def _secret_type(secret_type):
    match secret_type:
        case 'excel':
            return Excel


class Secrets(metaclass=Singleton):
    def __init__(self):
        self._data_sources = {}

    def add_source(self, config_path):
        path = Path(config_path).resolve()
        try:
            conf = open(path)
        except IOError as e:
            log.error("An IOError occured: %s" % e)
            return
        with conf:
            config = json.load(conf)

        key = config['source']['name']
        if self.contains(key):
            return

        source = _secret_type(config['source']['type'])(path, config)

        self._data_sources[key] = source

    def get_data_source(self, source):
        return self._data_sources.get(source, None)

    def get_data_collection(self, source, collection):
        return self.get_data_source(source)\
            .from_collection(collection)

    def get_data_entry(self, source, collection, **selection):
        return self.get_data_collection(source, collection).select(**selection)

    def update_data_entry(self, entries, key, new_value):
        if isinstance(entries, list):
            for entry in entries:
                entry.update(key, new_value)
        else:
            entries.update(key, new_value)
        return entries

    def save_source_changes(self, source):
        s = self.get_data_source(source)
        s.save_changes()

    def contains(self, key):
        return key in self._data_sources

    def is_empty(self):
        if not bool(self._data_sources):
            return True
        return False
