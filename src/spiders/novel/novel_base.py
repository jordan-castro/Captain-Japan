from src.spiders.base import BaseScraper, Tag, Website, ScrapeType
import time


class NovelSpider(BaseScraper):
    """
    The base spider for all Novels.

    Attributes:
        - chapters (list): A list of chapters.
        - website (Website): The website to scrape.

    # Properties:

    Methods:
        -> check Base

    """
    def __init__(self, website: Website, debug: bool = False) -> None:
        self.chapters = []
        super().__init__(website, debug=debug)

    def search_title(self, title, source):
        # Search on Google for the title with the source.
        # For example, "The Second Coming of Gluttony, TSCOG, etc" as the title.
        # The source being the website so "Wuxia World".
        # We will grab the first result so long as it matches the HREF of the website base_url.
        self.change_page(f"https://www.google.com/search?q={title} {source}")
        time.sleep(1)
        google_search = self.soup_object

        # Scrape the page for all the results.
        results = google_search.find_all("div", class_="g")
        for result in results:
            # Check the HREF of the result.
            # It must match the base_url of the website.
            href = result.find("a")["href"]
            if href.startswith(self.base_url):
                # The result is a match.
                # Return the HREF.
                return href
        print(f"Could not find {title} with source {source}")

    def load_chapters(self):
        super().load_chapters()

    def build_url(self, chapter):
        super().build_url(chapter)

    def scrape(self, page):
        super().scrape(page)


if __name__ == "__main__":
    website = Website("https://www.wuxiaworld.com", None, None, None, None, ScrapeType.NOVEL)
    spider = NovelSpider(website)

    spider.search_title("The Second Coming of Gluttony", "Wuxia World")