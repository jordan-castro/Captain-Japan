from pathlib import Path
from cj.utils.settings import read_settings
import shutil
import os 
import glob


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

    shutil.rmtree(path)


def replace_directory(path):
    """
    Replace a directory. Basically recreate it.

    Params:
        - path(str): The path to the directory to replace.
    """
    # Get the path
    p = Path(path)

    # Check if the directory exists
    if p.exists() is False:
        # Just create it then
        create_dir(path)
        # Close function
        return

    # Delete the directory
    delete_directory(path)

    # Create the directory
    create_dir(path)


def create_source_path(source, dir):
    """
    Create the directories of a novel.
    
    Params:
        - source: The source to create the directories for.
        - dir(str): The directory to create the directories in.
    """
    # Convert the title to only capital letters for the first letter
    title = ""
    title_split = source.title.split(' ')
    for word in title_split:
        space = " " if title_split.index(word) > 0 else ""
        letters = [letter for letter in word]
        letters[0] = letters[0].upper()
        title += space + ''.join(letters)
    
    # Get the source path
    source = read_settings("path")['source'] + f'/{dir}/{title}'
    # Create the novel directory
    create_dir(source)
    return source


def change_path_if_already_exists(path) -> str :
    """
    Change the path if the file already exists. 

    Params:
        - <path: str> The path to the file or folder.

    Returns:
        - <path: str> The path to the file or folder.
    """
    p = Path(path)
    # Check if it even exists first of all
    if p.exists() is False:
        # Return the original path
        return path

    # Ok it does exist, so let's find out how many times it exists
    name = path.split(get_slash_type(path))[-1]
    extension = name.split('.')[-1]
    # Get the path without the name
    path = path.replace(name, '')
    # Get the number of files with the same name
    files = glob.glob(path + '*')
    count = 0
    # Remove the extension
    name = name.replace(f'.{extension}', '')

    for file in files:
        if name.lower() in file.lower():
            count += 1
    
    # Add the number to the name
    name = name + f'_{count}.{extension}'

    return path + name


def get_slash_type(path)-> str :
    """
    Get the slash type of a path.

    Returns:
        - string
    """
    if '\\' in path:
        return '\\'
    else:
        return '/'


def get_files_in_directory(path) -> list[str]:
    """
    Get all the files in a directory.
    """
    files = glob.glob(f"{path}/*")

    return files