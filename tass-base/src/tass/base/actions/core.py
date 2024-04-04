from ..core.valuestore import ValueStore
from ..core.secrets import Secrets


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
    """Add a new data source from a configuration file.

    If a source with the same name exists,
    new source is not loaded.

    Args:
        config_path:
            The file path to the json format
            configuration for the new data source.
    """
    secrets = Secrets()

    secrets.add_source(config_path)


def update_data_entry(key, new_value, stored_filter=None, **secret):
    """Update an existing data entry in memory.

    Updated entries are only changed in memory,
    to save changes to the source use save_data_source.

    Args:
        key:
            The str key or column label for the
            entries to be updated.
        new_value:
            The new value to change the selected
            column to. If changing multiple entries
            the same value is assigned to each.
        stored_filter:
            The tuple defining the source and saved
            filter name if using a saved filter.
        secret:
            If not using a saved filter can specify
            the filters to be applied to locate
            desired entries.
    """
    secrets = Secrets()
    if (stored_filter):
        _filter = secrets.get_data_source(
            stored_filter[0]).filters[stored_filter[1]]
    else:
        _filter = secret
    entry = secrets.get_data_entry(**_filter)

    secrets.update_data_entry(entry, key, new_value)


def save_data_source(source):
    """Save the specified source to file.

    Args:
        source:
            The name of the source to save.

    """
    secrets = Secrets()
    secrets.save_source_changes(source)


def store_secret_value(key, value_key, stored_filter=None, **secret):
    """Store a value from an entry.

    Get a value from an entry and store it using
    ValueStore. The filter used must return exactly
    1 entry.

    Args:
        key:
            The str key to store the value under.
        value_key:
            The column key to read the value from.
        stored_filter:
            The tuple defining the source and saved
            filter name if using a saved filter.
        secret:
            If not using a saved filter can specify
            the filters to be applied to locate
            desired entries.
    Raises:
        TypeError:
            If the filter returns multiple entries
            a TypeError is raised.
    """
    store = ValueStore()
    secrets = Secrets()

    if (stored_filter):
        _filter = secrets.get_data_source(
            stored_filter[0]).filters[stored_filter[1]]
    else:
        _filter = secret
    data = secrets.get_data_entry(**_filter)

    if isinstance(data, list) and data.len() > 1:
        raise TypeError("""Can only store data from a single entry.
        Filter must have count of 1.""")
    store.add_to_dict(key, data.get(value_key))
