import json
from pathlib import Path


class DataSource():

    def __init__(self, config):
        self._config = config
        
    
class Collection():
    def __init__(self, *args, **kwargs):
        self._entries = self._load_entries(*args, **kwargs)
        
    def _load_entries(self, *args, **kwargs):
        raise NotImplementedError("Please implement this function.")

class Entry():
    def __init__(self, data):
        self._data = data