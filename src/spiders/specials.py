class Specials(object):
    """
    Holds methods for the Base spiders to do special things 
    depending on if they need to or not.

    Attributes:
        search_title (function):
            Searches for the title of the source.
        load_chapters (function):
            Loads the chapters of the source.
        build_url (function):
            Builds the url of the source.
        scrape (function):
            Scrapes the source.
    """
    def __init__(self, search_title=None, load_chapters=None, build_url=None, scrape=None):
        self.search_title = search_title
        self.load_chapters = load_chapters
        self.build_url = build_url
        self.scrape = scrape

