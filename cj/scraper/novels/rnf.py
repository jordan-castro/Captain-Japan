# A WEB SCRAPER for ReadNovelFull.com

from typing import KeysView
from cj.scraper.novel_base import NovelBase
from selenium.webdriver.common.by import By

from cj.objects.chapter import Chapter


class RNF(NovelBase):
    """
    This class handles the ReadNovelFull scraping.
    """

    def __init__(self, title: str) -> None:
        super().__init__(True, True, "https://readnovelfull.com", title)

    def cover(self) -> str:
        cover_loc = '//*[@id="novel"]/div[1]/div[1]/div[2]/div/div[2]/img'
        try:
            # Get with selenium
            cover_url = self.driver.find_element(By.XPATH, cover_loc).get_attribute("src")
            # Return the cover url
            return cover_url
        except:
            print(f"Error getting cover for {self.title}")
            return None

    def load_chapters(self, url: str) -> None:
        chapters_loc = 'panel-body'
        # Go to the url passed
        self.current_url = url + "#tab-chapters-title"
        try:
            # Get a soup object
            soup = self.soup()
            # Get the chapters
            chapters_holder = soup.find('div', {'class': chapters_loc})
            # Get the chapters rows here
            chapters_rows = chapters_holder.find_all('div', {'class': 'row'})
            # Loop through the rows
            for row in chapters_rows:
                # Get the li tags
                li_tags = row.find_all('li')
                for li in li_tags:
                    # 'a' stangs for the anchor tags
                    a = li.find('a')
                    # Get the chapter url 'href' and title
                    chapter_href = a.get('href')
                    chapter_title = a.get('title')
                    # Get the chapter number
                    chapter_number = self._format_chapter_number(chapter_title, len(self.chapters))
                    # Add this chapter to the chapters list
                    chapter = Chapter(chapter_href, chapter_number, chapter_title)
                    self.chapters.append(chapter)
        except Exception as e:
            print("Error is {}".format(e))
            # Just end the function here but print that it did not work
            print(f"Could not find chapters for {self.title} at {url}")
            return

    # TODO: NLP
    def _format_chapter_number(self, chapter_title: str, index: int) -> int:
        """
        Format the number of the chapter.

        Params:
            - chapter_title(str): The title of the chapter.
            - index(int): The index of the chapter, what we might fall back on.

        Returns:
            - int the chapter number
        """
        return index
        # # Check if the chapter title is a number
        # if chapter_title.isnumeric():
        #     return int(chapter_title)
        
        # # Find the first set of numbers in the chapter title
        # chapter_split = chapter_title.split(" ")
        # # Loop through the split
        # for data in chapter_split:
        #     # Check if is numeric
        #     if data.isnumeric():
        #         return int(data)

    def scrape(self, chapter: Chapter) -> Chapter:
        chapter_container = {
            "tag": "div",
            "selector": "id",
            "value": "chr-content",
            "text": {
                "tag": "p",
            }
        }
        # build the url
        url = self.build_url(chapter.number)

        self.set_should_scroll(True)
        self.set_scroll_distance(1000)
        # Go to the url
        soup = self.get_chapter(url)
        # Check if soup is None
        if soup is None:
            return None

        # Get the chapter content
        chapter_content = soup.find(
            chapter_container["tag"],
            {
                chapter_container["selector"]: chapter_container["value"]
            }
        )
        # Get the body 
        body = chapter_content.find_all(chapter_container["text"]["tag"])
        chapter.document = body
        chapter.body = ""
        # Get the text
        for text in body:
            chapter.body += text.text.strip() + "\n\n"
        # Return the text
        return chapter

    def build_url(self, chapter: int) -> str:
        # Check that the chapter number is in the list
        if chapter >= len(self.chapters) or chapter < 0:
            raise ValueError(f"Chapter number {chapter} is out of range")

        # Return the chapter url
        return self.base_url + self.chapters[chapter].url

    def search(self) -> str:
        search_field = None
        try:
            search_field = self.driver.find_element(By.ID, "search-input")
        except:
            return None
        # Input the search query
        search_field.send_keys(self.title)
        # Enter the search query
        search_field.submit()
        # Wait for the search results to load
        self.set_should_wait(True)
        self.set_wait_time(5)
        self.wait()

        # Lets get the results
        novel_titles = self.driver.find_elements(By.CLASS_NAME, "novel-title")

        # Loop through the results
        for novel_title in novel_titles:
            # Check if the novel title is similar to the title we are looking for
            if self.title.lower() in novel_title.text.lower():
                # Get the novel url
                novel_url = novel_title.find_element(By.TAG_NAME, "a").get_attribute("href")
                # Return the novel url
                return novel_url
        
        # Could not find the novel
        return None