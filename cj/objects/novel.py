from cj.data.conn import COL_NOVEL_ID, COL_NOVEL_TITLE, COL_NOVEL_LOCATION, COL_NOVEL_COVER
from cj.utils.json import from_json, to_json


class Novel(object):
    _id: int = None
    title: str = None
    location: str = None
    cover: str = None

    def __init__(self, id: int, title: str, location: str, cover: str) -> None:
        self._id = id
        self.title = title
        self.location = location
        self.cover = cover

    def __str__(self) -> str:
        return f"Novel: {self.title}"
    
    def __repr__(self) -> str:
        return f"Novel(id={self._id}, title={self.title}, location={self.location}, cover={self.cover})"
    
    def __eq__(self, other: object) -> bool:
        return self._id == other._id and self.title == other.title and self.location == other.location and self.cover == other.cover

    @staticmethod
    def from_json(json):
        """
        Create a Novel object from some json (dict) data. Works really well with SQL queries as well.

        Params:
            - json(str): The json (dict).

        Returns:
            - Novel
        """
        return from_json(json, Novel)
        # return Novel(
            # json[COL_NOVEL_ID],
            # json[COL_NOVEL_TITLE],
            # json[COL_NOVEL_LOCATION],
            # json[COL_NOVEL_COVER]
        # )

    def to_json(self):
        """
        Create a json (dict) from a Novel object.

        Returns:
            - dict
        """
        data = {
            COL_NOVEL_ID: self._id,
            COL_NOVEL_TITLE: self.title,
            COL_NOVEL_LOCATION: self.location,
            COL_NOVEL_COVER: self.cover
        }

        return to_json(data)