from backend.generator.epub_generator import generate_epub
from backend.utils.default_title import default_title
from backend.generator.pdf_generator import generate_pdf
from backend.utils.downloader import download_novel
from backend.scraping.req import make_GET_request, valid_url
from bs4 import BeautifulSoup
from backend.scraping.soup_find_text import find_text
from backend.browser.browse import InteractiveBrowser


class WuxiaScraper:
    def __init__(self, connection=None):
        # Wuxia URL
        self.wuxia_url = "https://www.wuxiaworld.com/"
        self.browser = connection or InteractiveBrowser(self.wuxia_url)
        # Each novel has its own way of defining their chapters url path.
        # It is det in find_novel()
        self.chapters_path = None
        # Also set in find_novel()
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
        # Chequea que encontramos el buton
        if len(chapters_button) == 0:
            return False
        chapters_button[0].click()

        chapters = self.browser.grab_data_from_tags(("class", "chapter-item"))
        # Chequea que encontramos los capitulos
        if len(chapters) == 0:
            return False
        chapters[0].click()

        # Now we have the URL for the chapters
        self.chapters_path = self.browser.current_url().split("/")[-1].split("-chapter-")[0]
        
        return True

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

    def scrape(self, chapter):
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
        # Grab chapter_body
        chapter_body = soup.find(id="chapter-outer")
        chapter_text = chapter_body.find_all("p")

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
    found = wuxia.find_novel("The second coming of gluttony")

    if not found:
        print(f"Failed finding {wuxia.novel_title}")
        exit(0)

    chapters = []
    for x in range(8, 50):
        chapters.append(x + 1)
    downloads = download_novel(wuxia.novel_title, chapters, wuxia.scrape)
    
    files = [download.location for download in downloads]
    generate_epub(files, f"{default_title(wuxia.novel_title)}-epub")
    # generate_pdf(files, default_title(wuxia.novel_title))