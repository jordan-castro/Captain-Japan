from backend.data.helper import DOWNLOADS_TABLE, DbHelper
from backend.scraping.req import make_GET_request, valid_image_url
from multiprocessing.pool import ThreadPool
from bs4 import BeautifulSoup
from backend.browser.browse import InteractiveBrowser
from backend.data.models.download_model import Download
from backend.generator.generate_manga import generate_manga


class MangaKakalot:
    def __init__(self, connection=None):
        # MangaKakalot url
        self.kakalot_url = "https://mangakakalot.com/"
        self.browser = connection or InteractiveBrowser(self.kakalot_url)
        # Each manga has their own way of defining the series
        # Is defined in find_manga()
        self.manga_path = None
        self.manganato = False
        # Is also defined in find_manga()
        self.manga_title = None

    def find_manga(self, manga_title):
        """
        Find a manga on MangaKakalot web page.

        Params:
            - <manga_title: str> the title of the manga

        Return: <bool>
        """
        # Check if we are at the Kakalot url
        if self.browser.current_url() != self.kakalot_url:
            self.browser.change_page(self.kakalot_url)
        
        # Set title of manga
        self.manga_title = manga_title
        # Search for manga
        search_url = f"{self.kakalot_url}search/story/{self.manga_title.replace(' ', '_').lower()}"
        # Move to page
        self.browser.change_page(search_url)
        # Search page for tag
        story_titles = self.browser.grab_data_from_tags(("class", "story_name"))
        
        if len(story_titles) == 0:
            return False
        
        # Click the first one
        story_titles[0].find_element_by_tag_name('a').click()

        # We have the path now set it!
        self.manga_path = f"{self.browser.current_url()}"
        # Check if url contains readmanganato
        if "readmanganato" in self.manga_path:
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
            url = f"{self.manga_path}/chapter{seperater}{chapter}"
        else:
            seperater = "_"
            manga_id = self.manga_path.split('/')[-1]
            url = f"{self.kakalot_url}chapter/{manga_id}/chapter{seperater}{chapter}"

        return url

    def download(self, chapters):
        """
        Download the manga chapters passed.

        Params:
            - <chapters: list(int)> the chapters of the manga

        Important: Must call find_manga(self, manga_title) before calling, otherwise method will fail.

        Return: list(Download)
        """
        # Thread to save time
        pool = ThreadPool(processes=len(chapters))

        requests_ = []

        # Grab data
        for chapter in chapters:
            # Change to correct chapter
            self.browser.change_page(self.build_url(chapter))
            requests_.append(pool.apply_async(self.scrape_kakalot, (chapter, self.browser.get_page()))) # Todo 
        
        # Now loop through request_ and get data
        for request in requests_:
            # Data from request
            data = request.get()
            if not data:
                continue
            # Generate files
            paths = generate_manga(data, directory=f"{self.manga_title.replace(' ', '_')}")

        return list(
            map(
                lambda path: Download(
                    title=self.manga_title,
                    name=path.split('/')[-1].replace('.png', ''),
                    location=path,
                    image=None
                ), 
                paths
            )
        )

    def scrape_kakalot(self, chapter, page_content):
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

            print(f"El source del imagen es {image['src']}")

            image_data = make_GET_request(
                image['src'], 
                headers={"Referer": self.kakalot_url}
            )            
            chapter_images[chapter_images.index(image)] = image_data

        # Close internal browser

        return [
            chapter,
            chapter_images
        ]


if __name__ == "__main__":
    manga = MangaKakalot()
    hit = manga.find_manga("Return of the 8th class magician")
    if not hit:
        print(f"Could not find {manga.manga_title}")
    
    chapters = []

    for x in range(1):
        chapters.append(x+1)

    downloads = manga.download(chapters)
    db = DbHelper(True)

    for download in downloads:
        db.insert(DOWNLOADS_TABLE, download.sql_format())

    print(db.query_downloads())