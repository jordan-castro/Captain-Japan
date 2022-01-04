from abc import abstractmethod
from cj.objects.book import Book
from cj.utils.path import change_path_if_already_exists, get_slash_type
from cj.utils.settings import read_settings
import glob


class BookMaker:
    """
    Book maker is basically just a class that holds a bunch of data that a Book would need.
    ! Important, the BookMaker class does not actually make a book.
    """
    formatted_chapters: list = []
    path: str = None

    def __init__(self, chapters: list[str], book: Book, description: str = None) -> None:
        self.chapters = chapters
        self.book = book
        self.description = description
        self._create_file_path()

    @abstractmethod
    def make(self):
        """
        Make the Book!
        """
        raise NotImplementedError
    
    @abstractmethod
    def setup(self):
        """
        Setup the class objects for the instance of book maker.
        """
        raise NotImplementedError

    def _create_file_path(self):
        """
        Create the path to the book.
        """
        # First load in the book type
        book_type = self.book.book_type
        # Now find where does this book belong from settings
        where_it_belongs = read_settings("path")[str(book_type)] + "/"
        # Set the path.
        self.path = change_path_if_already_exists(where_it_belongs + f"{self.book.title}.epub")
    

def get_chapters_for_maker(chapters: list[int], **kwargs):
    """
    Find the chapter locations for a Novel based on it's title.

    Params:
        - <chapters: list[int]> The chapters that are to be made into a book.

    Returns:
        - list[str] A list of the locations for the chapters.
    """
    if "title" in kwargs.keys():
        novel_location = read_settings("path")["source"] + f"/novels/{kwargs['title']}/"
    else:
        novel_location = kwargs['location'] + '/'

    chapter_locations = []

    for chapter in chapters:
        # Add to the folder
        chapter_location = novel_location + f"{chapter}/"
        # Glob the chapter location
        chapter_html = glob.glob(chapter_location + "*.html")
        chapter_locations.append(chapter_html[0])

    return chapter_locations