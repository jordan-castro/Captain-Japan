from selenium.webdriver.common.by import By
from src.spiders.base import BaseScraper, Tag, Website, ScrapeType
import time

from src.spiders.specials import Specials


class NovelSpider(BaseScraper):
    """
    The base spider for all Novels.

    Attributes:
        - chapters (list): A list of chapters.
        - website (Website): The website to scrape.
        - specials (Specials): The specials to scrape.

    # Properties:

    Methods:
        -> check Base

    """
    def __init__(self, website: Website, specials: Specials, debug: bool = False) -> None:
        self.chapters = []
        self.specails = specials
        super().__init__(website, debug=debug)

    def search_title(self, title, source):
        if self.specails.search_title:
            self.specails.search_title(title, source)
        # Search on Google for the title with the source.
        # For example, "The Second Coming of Gluttony, TSCOG, etc" as the title.
        # The source being the website so "Wuxia World".
        # We will grab the first result so long as it matches the HREF of the website base_url.
        self.change_page(f"https://www.google.com/search?q={title} {source}")
        google_search = self.soup_object

        url = None
        # Scrape the page for all the results.
        results = google_search.find_all("div", class_="g")
        for result in results:
            # Check the HREF of the result.
            # It must match the base_url of the website.
            href = result.find("a")["href"]
            if href.startswith(self.website.base_url):
                # The result is a match.
                url = href
        if not url:
            print(f"Could not find {title} with source {source}")
            return
        # Change the page to the result.
        self.change_page(url)
        print(self.get_chapter_links())
        
    def load_chapters(self):
        if self.specails.load_chapters:
            self.specails.load_chapters()

        # Grab all the chapters from the website.
        # The chapters are found based on the Tag.
        chapters_page = self.soup_object

        # Scrape the page for all the chapters.
        chapters = chapters_page.find_all(self.website.chapters_tag.tag_type, self.website.chapters_tag.tag_value)
        print("Nigga chapters ", chapters)

    def build_url(self, chapter: int):
        if self.specails.build_url:
            self.specails.build_url(chapter)

        # Return the URL of the chapter.
        # Find the chapter in the list of chapters.
        # If the chapter is not in the list, return None.
        if self.chapters[chapter]:
            return self.chapters[chapter]

    def scrape(self, page):
        if self.specails.scrape:
            self.specails.scrape(page)


if __name__ == "__main__":
    title_tag = Tag(By.CLASS_NAME, "title", 'h3')
    description_tag = Tag(By.CLASS_NAME, "desc-text", 'div')
    chapters_tag = Tag(By.CLASS_NAME, 'list-chapter', 'ul')
    website = Website("https://novelfull.com/", title_tag, None, None, chapters_tag, description_tag, ScrapeType.NOVEL)
    spider = NovelSpider(website, Specials())

    spider.search_title("The Second Coming of Gluttony", "Read Novel Full")