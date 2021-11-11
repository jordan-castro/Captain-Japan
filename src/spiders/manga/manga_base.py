from src.spiders.base import BaseScraper, Tag, Website


class MangaSpider(BaseScraper):
    """
    The base spider for all Mangas.

    Attributes:
        - chapters (list): A list of chapters.
        - website (Website): The website of the manga.

    # Properties:

    Methods:
        -> Check Base
    
    """
    def __init__(self, website: Website, debug: bool = False) -> None:
        self.chapters = []
        super().__init__(website, debug=debug)

    def search_title(self, title, source):
        super().search_title(title, source)

    def load_chapters(self):
        super().load_chapters()

    def build_url(self, chapter):
        super().build_url(chapter)

    def scrape(self, page):
        super().scrape(page)
