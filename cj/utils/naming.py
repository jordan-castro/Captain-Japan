# Methods for naming in CaptainJapan
import re

from cj.utils.path import get_slash_type


def remove_chars(string: str) -> str:
    """
    Remove characters from a string.
    """
    # We want to remove :><,.?/\|"
    # We also want to remove any non-alphanumeric characters
    string = re.sub(r'[^\w\s]', '', string)
    string = re.sub(r'[\s]+', ' ', string)
    return string.strip()


def get_file_name(file_path: str, extension: bool = False) -> str:
    """
    Get the name of a file based on it's path.
    Also works to get a file with an extension if extension is passed as True.
    """
    slash = get_slash_type(file_path)

    file_name = file_path.split(slash)[-1]

    if extension:
        return file_name
    else:
        return file_name.split('.')[0]