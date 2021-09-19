from os import getcwd
import json


def app_settings():
    """
    Return a dictionary or the app settings json file.
    """
    settings = None
    with open(getcwd() + "/app_data.json", 'r') as settings_file:
        settings = json.load(settings_file)
    return settings