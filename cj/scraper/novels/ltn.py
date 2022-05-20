# Scraper for: https://www.ltnovel.com/

from cj.scraper.novel_base import NovelBase
from selenium.webdriver.common.by import By

from cj.objects.chapter import Chapter
from lxml import etree

class LTN(NovelBase):
    """
    This class handles scrapings for the LT Novel website.
    """
    def __init__(self, title: str, url) -> None:
        super().__init__(False, True, url, title)

    def cover(self) -> str:
        cover_xpath = '//*[@id="novel"]/header/div/div[1]/figure/img'
        # Try to grab the cover
        try:
            soup = self.soup()
            dom = etree.HTML(str(soup))
            cover_url = dom.xpath(cover_xpath)[0].get("src")
            return cover_url
        except:
            print(f"Error getting cover at {self.current_url}\nFor: {self.title}")
            return None

    def load_chapters(self, url: str) -> None:
        pass # This method is not used in LTN.

    def scrape(self, chapter: Chapter) -> Chapter:
        chapter_container = {
            "tag": "div",
            "selector": "class",
            "value": "chapter-content",
            "text": {
                "tag": "p",
            }
        }
        # Build the URL
        url = self.build_url(chapter.number)
        # Get a soup object and check that it worked
        soup = self.get_chapter(url)
        if soup is None:
            return None

        # Get the content of the chapter
        body = self.get_chapter_content(chapter_container, soup)
        chapter.body = ""
        chapter.document = ""
        # Get the text
        for text in body:
            chapter.body += text.text.strip() + "\n\n"
            chapter.document += text.prettify(formatter="html")
        # Return the chapter
        return chapter

    def build_url(self, chapter: int) -> str:
        # Add the chapter number to the url
        url = f"{self.base_url}_{chapter + 1}.html"
        return url
