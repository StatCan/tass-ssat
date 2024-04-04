class DataSource():

    def __init__(self, config_path, config):
        _source = config['source']

        self._name = _source['name']
        self._config_path = config_path
        self._load_datasource(config)
        self._load_saved_filters(config)
        self._changed = False

    def _load_datasource(self, config):
        raise NotImplementedError("Please implement this function.")

    def save_changes(self):
        raise NotImplementedError("Please implement this function.")

    def from_collection(self, collection):
        return self._collections[collection]

    def _load_saved_filters(self, config):
        filters = config.get('saved-filters', [])
        self._filters = {}
        for s_filter in filters:
            self._filters[s_filter['name']] = s_filter['filter']

    def update(self):
        self._changed = True

    @property
    def filters(self):
        return self._filters


class Collection():
    def __init__(self, parent, *args, **kwargs):
        self._entries = self._load_entries(*args, **kwargs)
        self._parent = parent
        self._changed = False

    def update(self):
        self._changed = True
        self._parent.update()

    def _load_entries(self, *args, **kwargs):
        raise NotImplementedError("Please implement this function.")

    @property
    def entries(self):
        return self._entries

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
                        if len(matches) == count:
                            break
            return matches


class Entry():
    def __init__(self, parent, data):
        self._data = data
        self._parent = parent
        self._changed = False

    def get(self, key):
        return self._data[key]

    def has(self, key):
        return key in self._data

    def update(self, key, new_value):
        if key in self._data:
            self._data[key] = new_value
            self._changed = True
            self._parent.update()

    @property
    def changed(self):
        return self._changed
