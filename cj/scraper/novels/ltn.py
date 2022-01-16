# Scraper for: https://www.ltnovel.com/

from cj.scraper.novel_base import NovelBase
from selenium.webdriver.common.by import By

from cj.objects.chapter import Chapter

class LTN(NovelBase):
    """
    This class handles scrapings for the LT Novel website.
    """

    def __init__(self, title: str) -> None:
        super().__init__(True, True, "https://www.ltnovel.com", title)

    def cover(self) -> str:
        cover_xpath = '//*[@id="novel"]/header/div/div[1]/figure/img'
        # Try to grab the cover
        try:
            cover_url = self.driver.find_element(By.XPATH, cover_xpath).get_attribute("src")
            return cover_url
        except:
            print(f"Error getting cover at {self.current_url}\nFor: {self.title}")
            return None

    def load_chapters(self, url: str) -> None:
        pass

    def scrape(self, chapter: Chapter) -> Chapter:
        pass

    def build_url(self, chapter: int) -> str:
        pass

    def search(self) -> str:
        # Lower the title and add "-" in place of spaces
        title = self.title.lower()
        title = title.replace(" ", "-")
        # Add to url
        url = self.base_url + f"/novel/{title}"
        # Go to the url
        self.get_url(url)

        # Check if a cover is found
        cover = self.cover()
        if cover is None:
            # The novel does not exist under that name.
            print(f"Novel {self.title} does not exist.")
            return None
        else:
            return url