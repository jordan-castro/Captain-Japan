from cj.utils.enums import BookType
from cj.utils.naming import remove_chars


class Book:
    title: str = None
    author: str = None
    location: str = None
    _type: BookType = None
    
    def __init__(self, title=None, author=None, location=None) -> None:
        self.title = title
        self.author = author
        self.location = location

    def __str__(self) -> str:
        return f"{self.title} by {self.author}"

    def __repr__(self) -> str:
        return f"{self.title} by {self.author}"
    
    def __eq__(self, other) -> bool:
        return self.title == other.title and self.author == other.author and self.location == other.location

    @property
    def book_type(self) -> BookType:
        """
        Get the book type from a location string.
        """
        # Check if we already have a type or what not.
        if self._type is not None:
            return self._type
        # Raise exception if location is None
        if self.location is None:
            raise ValueError("No Book location provided.")
        
        # Strip by the last . to get the extension
        extension = self.location.split(".")[-1]
        return BookType.from_str(extension)

    @property
    def _chapter_numbers(self):
        # Requires that the location is set
        if self.location is None:
            raise ValueError("No Book location provided.")
        
        # Get the chapter number from the location
        if '\\' in self.location:
            splitter = '\\'
        else:
            splitter = '/'
        
        # Get the last part of the location
        last_part = self.location.split(splitter)[-1]
        chapters = last_part.split('-')[-1]
        # Remove the ext
        chapters = chapters.split('.')[0]
        # Split again by _
        chapters = chapters.split('_')
        # Return the first part
        return [int(chapter.split()) for chapter in chapters]


    @property
    def starting_chapter(self) -> int:
        """
        Return the starting chapter of the book.
        """
        return min(self._chapter_numbers)

    @property
    def ending_chapter(self) -> int:
        """
        Return the ending chapter of the book.
        """
        return max(self._chapter_numbers)