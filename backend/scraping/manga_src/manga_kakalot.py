from backend.utils.downloader import download_manga
from bs4 import BeautifulSoup
from backend.browser.browse import InteractiveBrowser


class MangaKakalot:
    def __init__(self, connection=None):
        # MangaKakalot url
        self.kakalot_url = "https://mangakakalot.com/"
        self.browser = connection or InteractiveBrowser(self.kakalot_url, True)
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

    for x in range(10):
        chapters.append(x+1)

    download_manga(manga.manga_title, chapters, manga)

    # downloads = manga.download(chapters)
    # db = DbHelper(True)

    # for download in downloads:
    #     db.insert(DOWNLOADS_TABLE, download.sql_format())

    # print(db.query_downloads())