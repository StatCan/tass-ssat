from .singleton import Singleton

class ValueStore(metaclass=Singleton):
    def __init__(self):
        self.value_dict = {}

    def add_to_dict(self, key, value):
        self.value_dict[key] = value

    def get_data(self, key):
        return self.value_dict[key]

    def contains(self, key):
        return key in self.value_dict

    def is_empty(self):
        if not bool(self.value_dict):
            return True
        return False
