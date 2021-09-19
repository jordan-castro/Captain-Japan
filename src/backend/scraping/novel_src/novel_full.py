### Source to scraoe the ReadNovelFull.com website
from src.backend.utils.default_title import default_title
from src.backend.generator.epub_generator import generate_epub
from src.backend.utils.downloader import Downloader
from src.backend.scraping.scraper_base import Scraper
from src.backend.scraping.req import make_GET_request
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
import time


class ReadNovelFull(Scraper):
    def __init__(self, browser=None):
        self.chapter_paths = []
        super().__init__("https://readnovelfull.com", 0, True, browser)

    def find(self, novel_title):
        """
        Find the novel your looking to scrape.

        Params:
            - <novel_title: str> The title of the novel you are looking to scrape.

        Returns: <bool>
        """
        # Check if we are not at ReadNovelFull.com
        if self.current_url != self.source:
            self.change_page(self.source)
        
        # Set the title
        self.title = novel_title
        # Go to the novel
        novel_path = self.source + "/" + novel_title.replace(" ", '-') + ".html"
        self.change_page(novel_path)

        # Look for the READ NOW button
        elements = self.grab_data_from_tags(("class", "btn btn-danger btn-read-now"))
        # Check we did not get elements
        if not elements:
            # Add -novel at the enf of the url
            novel_path = self.source + "/" + novel_title.replace(" ", '-') + "-novel.html"
            self.change_page(novel_path)

        # Look for the READ NOW button
        elements = self.grab_data_from_tags(("class", "btn-read-now"))

        if not elements:
            # This time it did not work at all.
            return False

        # Click the first button
        elements[0].click()

        chapters_button = self.grab_data_from_tags(("class", "chr-jump"))
        if chapters_button:
            # Click and grab chapters
            chapters_button[0].click()
            # Espere un momento
            time.sleep(1)
            # Select
            select = Select(self.grab_data_from_tags(("class", "chr-jump"))[0])
            # Add the chapter paths!
            self.chapter_paths = list(
                map(
                    lambda option: option.get_attribute('value'),
                    select.options
                )
            )

        # Read the new url and set chapter path
        self.chapter_path = self.current_url()
        return True

    def build_url(self, chapter):
        """
        Build the url for the chapter passed.
        """
        if not self.chapter_paths:
            # Split the chapter path by it's -
            split_path = self.chapter_path.split('-')
            split_chapter = split_path[-1].split('.')
            # Edit split_chapter
            split_chapter[0] = str(chapter)
            # EDit split+path
            split_path[-1] = '.'.join(split_chapter)
            return '-'.join(split_path)
        else:
            return self.source + self.chapter_paths[chapter - 1]

    def scrape(self, chapter):
        """
        Scrape ReadNovelFull.com

        Params:
            - <chapter: int> The specific chapter to scrape.

        Returns: <dict>
        """
        # Build the url
        url = self.build_url(chapter)
        print(url)
        # Grab the page
        page = make_GET_request(url)
        # Start soup
        soup = BeautifulSoup(page.content, 'html.parser')
        # Find the chapter body
        chapter_body = soup.find(id='chr-content')
        # Make sure to grab chapter_body
        attempts = 1
        while attempts <= 10 and not chapter_body:
            # Rebuild the URl
            url = self.build_url(f'{chapter}{attempts}')
            # Grab contents
            page = make_GET_request(url)
            # Re build the Soup object
            soup = BeautifulSoup(page.content, 'html.parser')
            chapter_body = soup.find(id='chr-content')
            # Add one to attempts
            attempts += 1

        chapter_text = chapter_body.find_all('p')
        # Find the chapter title
        chapter_title = soup.find(class_='chr-text')

        data = {
            'chapter_text': chapter_text
        }

        # Chequea que tocamos a chapter_title
        if chapter_title:
            data['chapter_title'] = chapter_title.text

        # Now return
        return data


if __name__ == "__main__":
    nvfull = ReadNovelFull()
    hit = nvfull.find("The second coming of gluttony")
    chapters = list(range(149, 200))
    
    d = Downloader()
    downloads = d.download(nvfull.title, chapters, nvfull, 0)
    
    # files = [download.location for download in downloads]
    # generate_epub(files, f'{default_title(nvfull.title)}-epub-3')