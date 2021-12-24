import json
from typing import Any


SETTINGS_FILE = "cj/data/app.json"


def read_settings(key: str) -> Any:
    """
    Read the settings.

    Params:
        - key(str): The key to read the JSON from

    Returns:
        - value(Any)
    """
    # Read the settings file
    with open(SETTINGS_FILE, 'r') as file:
        settings = json.load(file)

        # Check if the key even exists
        if key not in settings:
            return None

        return settings[key]


def set_settings(key: str, value):
    """
    Set a setting.

    Params: 
        - key(str): The key to set.
        - value(Any): The value to set.
    """
    # Read the settings file
    with open(SETTINGS_FILE, 'r') as file:
        settings = json.load(file)

    settings[key] = value

    # Write the settings file
    with open(SETTINGS_FILE, 'w') as file:
        json.dump(settings, file)