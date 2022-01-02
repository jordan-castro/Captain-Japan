from cj.data.conn import COL_NOVEL_ID, COL_NOVEL_TITLE, COL_NOVEL_LOCATION, COL_NOVEL_COVER
from cj.objects.source import Source
from cj.utils.enums import CjType
from cj.utils.json import to_json


class Novel(Source):
    _id: int = None
    title: str = None
    location: str = None
    cover: str = None

    def __init__(self, id: int, title: str, location: str, cover: str) -> None:
        super().__init__(id, title, location, cover)
        self.cj_type = CjType.NOVEL

    @staticmethod
    def from_json(json) -> Source:
        return Novel(
            json[COL_NOVEL_ID],
            json[COL_NOVEL_TITLE],
            json[COL_NOVEL_LOCATION],
            json[COL_NOVEL_COVER]
        )

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


if __name__ == "__main__":
    novel = Novel.from_json({
        'novel_id': 1,
        'title': 'The Hobbit',
        'location': 'http://www.example.com/hobbit.html',
        'cover': 'http://www.example.com/hobbit.jpg'
    })
    print(novel.cover)