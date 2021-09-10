from subprocess import call
from pathlib import Path
import os


def hide_dir(directory):
    """
    Hide a directory.

    Params:
        - <directorY: str> The directory to hide.
    
    Returns: <bool>
    """
    # Check that the directory exists
    if not Path(directory).exists():
        return False

    # Hide it
    call(["attrib", "+H", directory])
    return True


def create_if_missing(directory):
    """
    Create a directory if it does not exist.

    Params:
        - <directort: str> The directory to build perhaps.
    
    Returns: <bool> True created, False already exists.
    """
    if not Path(directory).exists():
        # Create
        os.mkdir(directory)
        return True
    else:
        # BAKA! It already exists
        return False