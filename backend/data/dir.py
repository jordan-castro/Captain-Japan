from os import getcwd


def base_dir():
    return f"{getcwd()}/backend/scraped_data/"


def novels_dir():
    return f"{base_dir()}novels/"


def manga_dir():
    return f"{base_dir()}manga/"


def anime_dir():
    return f"{base_dir()}anime/"
