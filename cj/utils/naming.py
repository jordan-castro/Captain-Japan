# Methods for naming in CaptainJapan
import re


def remove_chars(string: str) -> str:
    """
    Remove characters from a string.
    """
    # We want to remove :><,.?/\|"
    # We also want to remove any non-alphanumeric characters
    string = re.sub(r'[^\w\s]', '', string)
    string = re.sub(r'[\s]+', ' ', string)
    return string.strip()