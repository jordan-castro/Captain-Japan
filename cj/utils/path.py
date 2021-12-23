from pathlib import Path
from cj.objects.novel import Novel
from cj.utils.settings import read_settings


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


def create_novel_path(novel: Novel):
    """
    Create the directories of a novel.
    
    Params:
        - novel(Novel): The Novel to create the directories for.
    """
    # Get the novel path
    novel_path = read_settings("path")['source'] + f'/novels/{novel.title}'
    # Create the novel directory
    create_dir(novel_path)
    return novel_path


def create_chapter_path(chapter: int, parent: str):
    """
    Create the chapters of a parent (Novel, Manga, Anime)

    Params:
        - chapter(int): The chapter to create the directories for, this should be the index of the chapter.
        - parent(str): The parent directory to create the chapter directories in.
    """
    # Get the chapter path
    chapter_path = parent + f'/{chapter}'
    # Create the chapter directory
    create_dir(chapter_path)