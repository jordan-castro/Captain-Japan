from generator.text_gen import generate_text_file
from scraping.req import make_GET_request, valid_url
from bs4 import BeautifulSoup
from scraping.soup_find_text import find_text
from multiprocessing.pool import ThreadPool
from browser.browse import InteractiveBrowser
from data.helper import DOWNLOADS_TABLE, DbHelper
from data.models.download_model import Download
import time


class WuxiaScraper:
    def __init__(self, connection=None):
        # Wuxia URL
        self.wuxia_url = "https://www.wuxiaworld.com/"
        self.browser = connection or InteractiveBrowser(self.wuxia_url)
        self.chapters_path = None
        self.novel_title = None

    def find_novel(self, novel_title):
        """
        Find the novel onn the WuxiaWorld Page.

        Params:
            - <novel_title: str> the title of the novel to find
        """    
        # Check if we are not at self.wuxia_url
        if self.browser.current_url() != self.wuxia_url:
            self.browser.change_page(self.wuxia_url)

        self.novel_title = novel_title
        # Create the end of the url and then the url
        end_of_url = novel_title.replace(" ", "-").lower()
        url = f"{self.wuxia_url}novel/{end_of_url}"
        # Check if url exists
        if not valid_url(url):
            return False

        # Change url
        self.browser.change_page(url)

        # Click chapters_button
        chapters_button = self.browser.grab_data_from_tags(("x-path", '//*[@id="content-container"]/div[4]/div/div/div[2]/div[3]/ul/li[2]/a'))
        chapters_button[0].click()

        chapters = self.browser.grab_data_from_tags(("class", "chapter-item"))
        chapters[0].click()
        # Now we have the URL for the chapters
        self.chapters_path = self.browser.current_url().split("/")[-1].split("-chapter-")[0]

    def build_url(self, chapter, return_url=False):
        """
        Build the url based on the chapter passed. 
        Will go to url for you, unless return_url is passed as True.

        Params:
            - <chapter: int> The chapter to build url from
            - <return_url: str> Whether or not to return the url built.

        Returns: <str | None>
        """
        url = self.novel_title.replace(" ", "-").lower()
        # Url with chapter number
        url_with_chapter_number = f"{self.wuxia_url}novel/{url}/{self.chapters_path}-chapter-{chapter}"
        if return_url:
            return url_with_chapter_number
        else:
            self.browser.change_page(url_with_chapter_number)

    def download(self, chapters):
        """
        Download the chapters passed.

        Params:
            - <chapters: list(int)> The list of chapters to download.
            - <one_file: bool=True> Split each chapter to its own file? 
            
        Important: Must call find_novel(novel_title) before in order to set up path and stuff

        Retunr: <list(Downloads)>
        """
        # Start the threading process
        pool = ThreadPool(processes=len(chapters))

        downloads = []
        requests_ = []
        
        # Grab chapter data
        for chapter in chapters:
            # Async scrape to make faster
            requests_.append(pool.apply_async(self.scrape_wuxia, (chapter,)))

        # Now loop and grab data from requests
        for request in requests_:
            # Data from request
            data_from_request = request.get()
            # File name
            file_name = f"Chapter_{chapters[requests_.index(request)]}"
            # Write to file
            file_path = generate_text_file(data_from_request, f"{file_name}", directory=self.novel_title)
            # Append data
            downloads.append(
                Download(
                    self.novel_title, 
                    file_name, 
                    int(time.time()), 
                    file_path, 
                    None
                )
            )

        # Return the downloads list
        return downloads

    def scrape_wuxia(self, chapter):
        """
        Scrape the Wuxia World website based on the tile of the series and chapter numbers.

        Params:
            - <chapter: int> the chapter to scrape

        Returns: <data: dict>  
        """
        # Build the URL
        url = self.build_url(chapter, return_url=True)
        # Grab page
        page = make_GET_request(url)
        # Start souper
        soup = BeautifulSoup(page.content, "html.parser")
        # Grab chapter text
        chapter_text = soup.find_all(dir="ltr")
        # Check that chapter_text is empty
        if len(chapter_text) < 1:
            chapter_text = soup.find_all("p")
            # self.strip_p_tag(chapter_text)

        # Grab chapter title
        chapter_title = soup.find_all(
            "h4", 
            string=lambda text: find_text(text, "Chapter")
        )[0].text.strip()

        data = {
            "chapter_title": chapter_title,
            "chapter_text": chapter_text
        }

        return data


if __name__ == "__main__":
    wuxia = WuxiaScraper()
    wuxia.find_novel("OVERGEARED")
    chapters = []
    for x in range(10):
        chapters.append(x + 1)
    downloads = wuxia.download(chapters)
    
    db = DbHelper()

    for download in downloads:
        db.insert(
            DOWNLOADS_TABLE, 
            download.sql_format()
        )

    print(db.query_downloads())

    # Close connection
    wuxia.browser.close_con()