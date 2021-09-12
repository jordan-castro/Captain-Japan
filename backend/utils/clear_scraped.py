### Script to clean the project of all scraped data. Mainly used for testing.
import os
import shutil
from backend.data.dir import manga_dir, novels_dir, anime_dir


def clean_project():
    """
    Remove all scraped data files.
    
    png/jpg - Yes
    html/xhtml - Yes
    epub/pdf - Yes
    mp4-oob - Yes
    """
    # Remove the directories
    for x in range(2):
        user = x == 1

        remove(manga_dir(user))
        remove(manga_dir(user))

        remove(novels_dir(user))
        remove(novels_dir(user))

        remove(anime_dir(user))
        remove(anime_dir(user))


def remove(dir):
    for root, dirs, files in os.walk(dir):
        for f in files:
            os.unlink(f)
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))


if __name__ == "__main__":
    clean_project()