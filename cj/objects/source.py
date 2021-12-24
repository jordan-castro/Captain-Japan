from abc import abstractmethod
from cj.utils.enums import CjType


class Source(object):
    _id: int = None
    title: str = None
    location: str = None
    cover: str = None
    cj_type: CjType = None

    def __init__(self, id: int, title: str, location: str, cover: str) -> None:
        self._id = id
        self.title = title
        self.location = location
        self.cover = cover

    def __str__(self) -> str:
        return f"Source: {self.title}"
    
    def __repr__(self) -> str:
        return f"Source(id={self._id}, title={self.title}, location={self.location}, cover={self.cover})"
    
    def __eq__(self, other: object) -> bool:
        return self._id == other._id and self.title == other.title and self.location == other.location and self.cover == other.cover

    @staticmethod
    def from_json(json):
        """
        Create a Source object from some json (dict) data. Works really well with SQL queries as well.

        Params:
            - json(str): The json (dict).

        Returns:
            - Source
        """
        raise NotImplementedError

    @abstractmethod
    def to_json(self):
        """
        Create a json (dict) from the Source object.

        Returns:
            - dict
        """
        raise NotImplementedError    

    def directory(self) -> str:
        """
        Return the directory of the source, i.e. if cj_type is CjType.NOVEL, the directory would be 'novels'.

        Returns:
            - str
        """
        # Trhow error if cj_type is not set
        if self.cj_type is None:
            raise ValueError("cj_type is not set")

        return self.cj_type.__str__().lower() + 's'

    def chapter_path(self, chapter_number) -> str:
        """
        Return the chapter path based on its number.

        Params:
            - chapter_number(int): The number of the chapter.

        Returns:
            - str
        """
        # Will raise error if location is not set
        if self.location is None:
            raise ValueError("location is not set")

        return f"{self.location}/{chapter_number}"