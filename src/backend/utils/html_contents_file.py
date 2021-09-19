### Script for when needing to create new scrapes.
import os


def write_contents(contents):
    with open(f"{os.getcwd()}/contents.html", 'w') as file:
        if type(contents) == list:
            for c in contents:
                file.write(str(c))
        else:
            file.write(contents)