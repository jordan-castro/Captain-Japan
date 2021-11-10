import enum

from src.spiders.tag import Tag


class ScrapeType(enum.Enum):
    MANGA = 0
    NOVEL = 1
    # ANIME = 2


class Website:
    """
    Data manager for a website.
    """
    def __init__(self, base_url, title_tag: Tag, body_tag: Tag, cover_image_tag: Tag, chapters_tag: Tag, scrape_type: ScrapeType) -> None:
        self.base_url = base_url
        self.title_tag = title_tag
        self.body_tag = body_tag
        self.cover_image_tag = cover_image_tag
        self.chapters_tag = chapters_tag
        self.scrape_type = scrape_type