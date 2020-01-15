import os
import json
from urllib.request import urlretrieve


def _get_data_path(data_path=None):
    """Return path to data dir.

    This directory stores large datasets required for the examples, to avoid
    downloading the data several times.

    By default the data dir is set to a folder named 'sg_template_data' in the
    user home folder.

    If the folder does not already exist, it is automatically created.

    Parameters
    ----------
    data_path : str | None
        The path to the data dir. ``~/sg_template_data`` by default.
    """
    if data_path is None:
        data_path = os.path.join('~', 'sg_template_data')
        data_path = os.path.expanduser(data_path)

    if not os.path.exists(data_path):
        os.makedirs(data_path)
    return data_path


def _get_config_path(config_path):
    """Return path to config file

    Parameters
    ----------
    config_path : str | None
        The path to the data dir. ``~/.sg_template`` by default.
    """
    if config_path is None:
        config_path = os.path.join('~', '.sg_template')
        config_path = os.path.expanduser(config_path)
    else:
        config_path = os.path.join(config_path, '.sg_template')
    return config_path


def _load_config(config_path):
    """Safely load a config file."""
    with open(config_path, 'r') as fid:
        try:
            config = json.load(fid)
        except ValueError:
            # No JSON object could be decoded --> corrupt file?
            msg = ('The config file ({}) is not a valid JSON '
                   'file and might be corrupted'.format(config_path))
            raise RuntimeError(msg)
            config = dict()
    return config


def _set_config(key, value, config_path=None):
    """Set the configurations in the config file.

    Parameters
    ----------
    key : str
        The preference key to set.
    value : str |  None
        The value to assign to the preference key. If None, the key is
        deleted.
    config_path : str | None
        The path to the .sg_template directory.
    """
    if not isinstance(key, str):
        raise TypeError('key must be of type str, got {} instead'\
            .format(type(key)))
    if not isinstance(value, str):
        raise TypeError('value must be of type str, got {} instead'\
            .format(type(value)))

    # Read all previous values
    config_path = _get_config_path(config_path)
    config_file = os.path.join(config_path, 'sg_template_config.json')

    if os.path.isfile(config_file):
        config = _load_config(config_file)
    else:
        config = dict()
    if value is None:
        config.pop(key, None)
    else:
        config[key] = value

    # Write all values. This may fail if the default directory is not
    # writeable.
    if not os.path.isdir(config_path):
        os.mkdir(config_path)
    with open(config_file, 'w') as fid:
        json.dump(config, fid, sort_keys=True, indent=0)


def download_data(url, data_file_name, data_path=None, config_path=None):
    """Downloads a remote dataset and saves path to config file.

    Fetch a dataset from ``url``, save to ``data_file_name`` in data_path, by
    default ``~/sg_template_data`` sand store the data location in config file,
    under key 'data_path'.

    Parameters
    ----------
    url : str
        Dataset URL.

    data_file_name : str
        File name to save the dataset at.

    data_path : str | None
        The path to the data dir. ``~/sg_template_data`` by default.

    config_path: str | None
        The path to the config file. ``~/.sg_template`` by default.

    Returns
    -------
    file_path : str
        Full path of the created file.
    """
    data_path = _get_data_path(data_path=data_path)
    file_path = os.path.join(data_path, data_file_name)
    # Download file if it doesn't exist
    if not os.path.exists(file_path):
        urlretrieve(url, file_path)
    # save download location in config
    _set_config('data_path', data_path, config_path)
    return file_path

def get_config(key, config_path=None):
    """Read configuration from config file.

    Parameters
    ----------
    key : str
        The configuration key to look for.

    config_path: str | None
        Path to the configuration file. ``~/.sg_template`` by default.

    Returns
    -------
    value : str | None
        The preference key value.
    """
    if not isinstance(key, str):
        raise TypeError('key must be of type str, got {} instead'\
            .format(type(key)))

    config_path = _get_config_path(config_path)
    config_file = os.path.join(config_path, 'sg_template_config.json')
    if os.path.isfile(config_file):
        config = _load_config(config_file)
    else:
        raise FileNotFoundError('The configuration file was not found: {}'\
            .format(config_file))
    return config[key]