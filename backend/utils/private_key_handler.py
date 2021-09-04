### Script that handles private keys.
from pathlib import Path
import os
from subprocess import call


def save_locally(user_id, key):
    """
    Create the file that is placed within a hidden folder in the app directory.

    Params:
        - <user_id: int> the id of the user
        - <key: str> the private key as a string

    Return: <str> file path
    """
    # First check if the directory does not exist
    if not Path("backend/.keys").exists():
        os.mkdir("backend/.keys")
    if not Path(f"backend/.keys/.{user_id}_sk").exists():
        os.mkdir(f"backend/.keys/.{user_id}_sk")
    
    path = f"backend/.keys/.{user_id}_sk/"

    # Hide paths # Todo Add other os's
    call(["attrib", "+H", "backend/.keys"])

    # Now create file
    with open(f"{path}{user_id}_skf.txt", "w") as skf:
        skf.write(str(key))

    # The path
    return f"{path}{user_id}_skf.txt"


def private_key(path):
    """
    Grab the private key based on the path to.

    Params:
        - <path: str> path to private key.

    Returns: <str|False>
    """
    # Check if path exists
    if not os.path.exists(path):
        return False

    # Grab-file and key
    with open(path, "r") as skf:
        return skf.read()


if __name__ == "__main__":
    # Set a private key from the local blockchain fork
    # This is not a REAL private key!!!
    save_locally(1, "0xea6385121ee52c5b7e8d65776663c14f43725b5d080d77dc3e778439815491c2")