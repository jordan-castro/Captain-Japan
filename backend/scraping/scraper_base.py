### The base of a scraper 
from abc import abstractmethod
from backend.browser.browse import InteractiveBrowser


class Scraper(InteractiveBrowser):
    """
    The base for all scraping objects.
    """

    def __init__(self, source, type, debug, browser):
        self.source = source
        self.type = type

        # Set in self.find()
        self.chapter_path = None
        self.title = None

        super().__init__(initial_url=source, debug=debug, browser=browser)

    @abstractmethod
    def find(self, title):
        pass

    @abstractmethod
    def scrape(self, chapter, page_content=None):
        pass

    @abstractmethod
    def build_url(self, chapter):
        pass