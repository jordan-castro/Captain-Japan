import enum
from julia import Main

from src.spiders.tag import Tag


class ScrapeType(enum.Enum):
    MANGA = 0
    NOVEL = 1
    # ANIME = 2


class Website:
    """
    Data manager for a website.
    """
    def __init__(
        self, 
        base_url, 
        title_tag: Tag, 
        body_tag: Tag, 
        cover_image_tag: Tag, 
        chapters_tag: Tag, 
        description_tag: Tag, 
        scrape_type: ScrapeType,
        chapters_args: dict=None
    ) -> None:
        self.base_url = base_url
        self.title_tag = title_tag
        self.body_tag = body_tag
        self.cover_image_tag = cover_image_tag
        self.chapters_tag = chapters_tag
        self.description_tag = description_tag
        self.scrape_type = scrape_type
        self.chapters_args = chapters_args
        
        self.__setup__()

    def __setup__(self):
        # Set up the julia scripts
        if self.chapters_args:
            Main.include("src/utils/WebsiteUtils.jl")


    def chapter_url(self, current_url) -> str:
        """
        Return the chapter url of the current url.

        Args:
            current_url (str): The current url.

        Returns: str 
        """
        return Main.chapterurl(current_url, self.chapters_args['types'], self.chapters_args['values'])