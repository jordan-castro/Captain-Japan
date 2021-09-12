from backend.utils.dir_helper import create_if_missing
from os import getcwd


### For the USER
def user_base_dir():
    create_if_missing(f"{getcwd()}/scraped")
    return f"{getcwd()}/scraped/"


def app_base_dir():
    return f"{getcwd()}/backend/scraped_data/"


def novels_dir(user=False):
    if user:
        path = f"{user_base_dir()}novels/"
    else:
        path = app_base_dir() + "novels/"

    create_if_missing(path)

    return path


def manga_dir(user=False):
    if user:
        path = f"{user_base_dir()}manga/"
    else:
        path = app_base_dir() + "manga/"

    create_if_missing(path)

    return path


def anime_dir(user=False):
    if user:
        path = f"{user_base_dir()}anime/"
    else:
        path = app_base_dir() + "anime/"
    
    create_if_missing(path)

    return path