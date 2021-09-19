from src.backend.utils.downloader import Downloader
from src.backend.scraping.scraper_base import Scraper
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from src.backend.scraping.req import make_GET_request


class MangaKakalot(Scraper):
    def __init__(self, browser=None):
        self.manganato = False
        super().__init__("https://mangakakalot.com/", 1, False, browser)

    def find(self, manga_title):
        """
        Find a manga on MangaKakalot web page.

        Params:
            - <title: str> the title of the manga

        Return: <bool>
        """
        # Check if we are at the Kakalot url
        if self.current_url() != self.source:
            self.change_page(self.source)

        # Set title of manga
        self.title = manga_title
        # Search for manga
        search_url = f"{self.source}search/story/{self.title.replace(' ', '_').lower()}"
        # Move to page
        self.change_page(search_url)
        # Search page for tag
        story_titles = self.grab_data_from_tags(("class", "story_name"))

        if len(story_titles) == 0:
            return False

        # Click the first one
        story_titles[0].find_element(By.TAG_NAME, 'a').click()

        # We have the path now set it!
        self.chapter_path = f"{self.current_url()}"
        # Check if url contains readmanganato
        if "readmanganato" in self.chapter_path:
            self.manganato = True

        return True

    def build_url(self, chapter):
        """
        Build the chapter url for the chapter passed.

        Params:
            - <chapter: int> the chapter.

        Return: <str> 
        """
        # Check if readmangano is tru
        if self.manganato:
            seperater = "-"
            url = f"{self.chapter_path}/chapter{seperater}{chapter}"
        else:
            seperater = "_"
            manga_id = self.chapter_path.split('/')[-1]
            url = f"{self.source}chapter/{manga_id}/chapter{seperater}{chapter}"

        return url

    def scrape(self, chapter, page_content):
        """
        Scrape a MangaKakalot manga chapter page.

        Params:
            - <chapter: int> the chapter to scrape.
            - <page_content: str> the content of the page

        Return: <dict>
        """
        # SOUPPY
        soup = BeautifulSoup(page_content, "html.parser")
        # Grab chapter body
        chapter_body = soup.find(class_="container-chapter-reader")
        # Grab images
        chapter_images = chapter_body.find_all("img")
        # Loop through images and screenshot
        for image in chapter_images:
            # Do some checking to make sure that the image source contains mangakakalot
            if not "mangakakalot" in image['src']:
                # delete from pile
                del chapter_images[chapter_images.index(image)]
                continue

            image_data = make_GET_request(
                image['src'],
                headers={"Referer": self.source}
            )
            chapter_images[chapter_images.index(image)] = image_data

        # Close internal

        return {
            "chapter_title": chapter,
            "chapter_body": chapter_images
        }


if __name__ == "__main__":
    manga = MangaKakalot()
    hit = manga.find("Return of the 8th class magician")
    if not hit:
        print(f"Could not find {manga.title}")

    chapters = []

    for x in range(10):
        chapters.append(x+1)

    downloader = Downloader()
    downloader.download(manga.title, chapters, manga, 1) 

    # downloads = download_manga(manga.title, chapters, manga)

    # files = [download.location for download in downloads]
    # generate_pdf(files, default_title(manga.title), manga=True)
    # generate_epub(files, f"{default_title(wuxia.novel_title)}-epub")

    # downloads = manga.download(chapters)
    # db = DbHelper(True)

    # for download in downloads:
    #     db.insert(DOWNLOADS_TABLE, download.sql_format())

    # print(db.query_downloads())
