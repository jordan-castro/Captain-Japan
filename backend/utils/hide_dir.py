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