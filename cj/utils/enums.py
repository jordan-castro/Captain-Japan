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