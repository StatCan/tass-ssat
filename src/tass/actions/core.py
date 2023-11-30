from tass.core.valuestore import ValueStore
from tass.core.secrets import Secrets


def store_value(key, value):
    """Store value for later access.

    Stores the given value in a dictionary
    using the given key. Overwrites
    any existing value for the provided key.

    Args:
        key:
            The unique key to be used as
            an accessor for the associated
            value. Must be a string.
        value:
            The value to be stored. The value
            can be any type.
    """
    ValueStore().add_to_dict(key, value)


def read_value(key):
    """Retrieve a previously stored value.

    Args:
        key:
            The string key that a
            value was stored with.

    Returns:
        The value that was stored using the given key.
        If the dictionary does not contain the given
        key then None is returned.
    """
    store = ValueStore()
    if store.contains(key):
        return store.get_data(key)
    else:
        return None

def add_data_source(config_path):
    secrets = Secrets()

    secrets.add_source(config_path)

def update_data_entry(key, new_value, stored_filter=None, **secret):
    secrets = Secrets()
    if (stored_filter):
        _filter = secrets.get_data_source(stored_filter[0]).filters[stored_filter[1]]
    else:
        _filter = secret
    entry = secrets.get_data_entry(**_filter)

    secrets.update_data_entry(entry, key, new_value)

def save_data_source(source):
    secrets = Secrets()
    secrets.save_source_changes(source)


def store_secret_value(key, value_key, stored_filter=None, **secret):
    store = ValueStore()
    secrets = Secrets()
    
    if (stored_filter):
        _filter = secrets.get_data_source(stored_filter[0]).filters[stored_filter[1]]
    else:
        _filter = secret
    data = secrets.get_data_entry(**_filter)

    store.add_to_dict(key, data.get(value_key))

    
