from enum import Enum


class CjType(Enum):
    NOVEL = 0
    MANGA = 1
    ANIME = 2

    def __str__(self):
        if self == CjType.NOVEL:
            return "novel"
        elif self == CjType.MANGA:
            return "manga"
        elif self == CjType.ANIME:
            return "anime"
        else:
            raise ValueError("Invalid CjType")


class BookType(Enum):
    EPUB = 0
    PDF = 1
    MOBI = 2
    HTML = 3

    def __str__(self):
        if self == BookType.EPUB:
            return "epub"
        elif self == BookType.PDF:
            return "pdf"
        elif self == BookType.MOBI:
            return "mobi"
        elif self == BookType.HTML:
            return "source"
        else:
            raise ValueError("Invalid BookType")
    
    @staticmethod
    def from_str(string: str):
        if string == "epub":
            return BookType.EPUB
        elif string == "pdf":
            return BookType.PDF
        elif string == "mobi":
            return BookType.MOBI
        elif string == "html":
            return BookType.HTML
        else:
            raise ValueError("Invalid BookType")