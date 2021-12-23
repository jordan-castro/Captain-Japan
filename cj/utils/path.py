from pathlib import Path


def create_dir(path):
    """
    Creates a directory if it does not exist.

    Params:
        - path(str): The path to the directory.
    """
    path = Path(path)

    # Check that path is a directory
    if not path.is_dir():
        return

    # Check if the directory exists
    if path.exists():
        return

    # Create the directory
    path.mkdir()