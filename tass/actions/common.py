from tass.core.valuestore import ValueStore


def store_value(key, value):
    ValueStore().add_to_dict(key, value)


def read_value(key):
    store = ValueStore()
    if store.contains(key):
        return store.get_data(key)
    else:
        return None
