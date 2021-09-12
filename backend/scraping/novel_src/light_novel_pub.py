### Scrape https://www.lightnovelpub.com/
from backend.generator.epub_generator import generate_epub
from backend.generator.pdf_generator import generate_pdf
from backend.utils.downloader import download_novel
from backend.browser.browse import InteractiveBrowser
from backend.utils.default_title import default_title
from bs4 import BeautifulSoup


class LightNovelPub(InteractiveBrowser):
    def __init__(self, debug=None, browser=None):
        # The initial URL
        self.pub_url = "https://www.lightnovelpub.com/search"
        
        # Declared in find_novel()
        self.chapter_path = None
        self.novel_path = None
        self.novel_title = None

        super().__init__(initial_url=self.pub_url, debug=debug, browser=browser)
        
    def find_novel(self, novel_title):
        """
        Find the novel and setup the class variables.

        Params: 
            - <novel_title: str> The title of the novel.

        Return: <bool>
        """
        # Check if we are not at the right url
        if self.current_url() != self.pub_url:
            self.change_page(self.pub_url)

        # The title of the novel default
        self.novel_title = default_title(novel_title)

        # Search the page and find the novel
        results = self.send_search(("id", "inputContent"), novel_title, ("class", "novel-item"))
        # Check that we got results
        if not results:
            # We could be on captcha.
            return False

        # We have results lets click the first one
        results[0].click()
        # Now grab current url
        self.novel_path = self.current_url()
        # Now grab chapters path
        self.chapter_path = self.novel_path + "/chapter-1"
        return True

    def build_url(self, chapter):
        """
        Build the lightnovel pub url based on the chapter passed.

        Params:
            - <chapter: int> The chapter to search url for.

        Return: <str> 
        """
        # Grab url as array
        url_arr = self.chapter_path.split('-')
        # Replace the last
        url_arr[-1] = f"{chapter}"

        # Now join to url
        url = "-".join(url_arr)
        return url

    def scrape(self, chapter):
        """
        Scrape the LightNovelPub website based on the chapter passed.

        Params:
            - <chapter: int> The chapter to scrape from.

        Return: <dict>
        """
        # Build the url
        url = self.build_url(chapter)
        # Move to page
        self.change_page(url)
        # print(self.get_page())
        # Souper
        soup = BeautifulSoup(self.get_page(), "html.parser")
        # Chapter container
        chapter_container = soup.find(id="chapter-container")

        # Clear the container
        for tag in chapter_container.find_all(class_="adsbox"):
            tag.extract()
        for tag in chapter_container.find_all(class_="fefafl"):
            tag.extract()
        for tag in chapter_container.find_all(class_="ipqtly"):
            tag.extract()
        for tag in chapter_container.find_all(class_="ihvwpp"):
            tag.extract()
        # Remove script tags
        for tag in chapter_container.select('script'):
            tag.extract()

        # Chapter title
        data = {
            # "chapter_title": chapter_title,
            "chapter_text": chapter_container
        }

        return data

if __name__ == "__main__":
    novel_pub = LightNovelPub()
    hit = novel_pub.find_novel("The beginning after the end")
    
    if not hit:
        print(hit)
        exit()

    chapters = []
    for x in range(20):
        chapters.append(x+1)
    
    downloads = download_novel(novel_pub.novel_title, chapters, novel_pub.scrape, async_=False)

    files = [download.location for download in downloads]
    generate_epub(files, default_title(novel_pub.novel_title))