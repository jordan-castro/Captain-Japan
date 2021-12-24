from pathlib import Path
from cj.utils.settings import read_settings
import os


def create_dir(path):
    """
    Creates a directory if it does not exist.

    Params:
        - path(str): The path to the directory.
    """
    path = Path(path)

    # Check if the directory exists
    if path.exists():
        return

    # Create the directory
    path.mkdir()


def delete_directory(path):
    """
    Delete a directory and it's contents.

    Params:
        - path(str): The path to the directory to delete.
    """
    p = Path(path)

    # Check if the directory does not exist
    if not p.exists():
        return

    # Delete the directory and it's contents
    os.rmdir(path, recursive=True)


def create_source_path(source, dir):
    """
    Create the directories of a novel.
    
    Params:
        - source: The source to create the directories for.
        - dir(str): The directory to create the directories in.
    """
    # Get the source path
    source = read_settings("path")['source'] + f'/{dir}/{source.title}'
    # Create the novel directory
    create_dir(source)
    return source