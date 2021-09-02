from generator.text_gen import generate_text_file
from scraping.req import make_GET_request
from bs4 import BeautifulSoup
from display.text import display_txt
from scraping.soup_find_text import find_text
from multiprocessing.pool import ThreadPool
from browser.browse import InteractiveBrowser


class WuxiaScraper:

    def __init__(self):
        # Wuxia URL
        self.wuxia_url = "https://www.wuxiaworld.com/"
        self.browser = InteractiveBrowser(self.wuxia_url)
        self.chapters_path = None
        self.novel_title = None

    def find_novel(self, novel_title):
        """
        Find the novel onn the WuxiaWorld Page.

        Params:
            - <novel_title: str> the title of the novel to find
        """    
        self.novel_title = novel_title
        # Create the end of the url
        end_of_url = novel_title.replace(" ", "-").lower()
        # Change url
        self.browser.change_page(f"{self.wuxia_url}novel/{end_of_url}")
        # Todo Check exists
        
        # Click chapters_button
        chapters_button = self.browser.grab_data_from_tags(("x-path", '//*[@id="content-container"]/div[4]/div/div/div[2]/div[3]/ul/li[2]/a'))
        chapters_button[0].click()

        chapters = self.browser.grab_data_from_tags(("class", "chapter-item"))
        chapters[0].click()
        # Now we have the URL for the chapters
        self.chapters_path = self.browser.current_url().split("/")[-1].split("-chapter-")[0]

    def build_url(self, chapter):
        """
        Build the url based on the chapter passed. Will go to url for you.

        Params:
            - <chapter: int> The chapter to build url from
        """
        url = self.novel_title.replace(" ", "-").lower()
        # Url with chapter number
        url_with_chapter_number = f"{self.wuxia_url}novel/{url}/{self.chapters_path}-chapter-{chapter}"
        self.browser.change_page(url_with_chapter_number)

    def download(self, chapters, one_file=True):
        """
        Download the chapters passed.

        Params:
            - <chapters: list(int)> The list of chapters to download.
            - <one_file: bool=True> Split each chapter to its own file? 
            
        Important: Must call find_novel(novel_title) before in order to set up path and stuff

        Return: <path_to_file: str|list> generated file path|paths
        """
        # Start the threading proccess
        pool = ThreadPool(processes=len(chapters))

        file_data = []
        requests_ = []
        
        # Grab chapter data
        for chapter in chapters:
            # Async scrape to make faster
            requests_.append(pool.apply_async(self.scrape_wuxia, (chapter,)))

        # Now loop and grab data from requests
        for request in requests_:
            # Data from request
            data_from_request = request.get()
            if one_file:
                file_data.append(data_from_request)
            else:
                # File name
                file_name = f"{self.novel_title} Chapter: {chapters[requests_.index(request)]}"
                # Add file name to list
                file_data.append(file_name)
                # Write to file
                generate_text_file([data_from_request], file_name)
                pass
        
        # Check to put in one file
        if one_file:
            # Flatten data
            flat_file_data = [chapter for inter in file_data for chapter in inter]
            # Generate file
            generate_text_file(flat_file_data, self.novel_title)

        if one_file:
            return f"{self.novel_title}.txt"
        else:
            return file_data

    def scrape_wuxia(self, chapter):
        """
        Scrape the Wuxia World website based on the tile of the series and chapter numbers.

        Params:
            - <chapter: int> the chapter to scrape

        Returns: <data: dict>  
        """
        # Build the URL
        self.build_url(chapter)
        # Grab page
        page = self.browser.get_page()
        # Start souper
        soup = BeautifulSoup(page, "html.parser")
        # Grab chapter text
        chapter_text = soup.find_all(dir="ltr")
        # Check that chapter_text is empty
        if len(chapter_text) < 1:
            chapter_text = soup.find_all("p")

        # Grab chapter title
        chapter_title = soup.find_all(
            "h4", 
            string=lambda text: find_text(text, "Chapter")
        )[0].text.strip()

        data = [
            {
                "chapter_title": chapter_title,
                "chapter_text": chapter_text
            }
        ]

        return data

# def scrape_wuxia(title, chapters):
#     """
#     Scrape the Wuxia World website based on the title of the series and chapter numbers.

#     Params:
#         - <title: str> The title of the series
#         - <chapters: list|int> A list of chapter numbers or one chapter

#     Return: <success: bool>
#     """
#     # Data to send to generator
#     data = []

#     # Scrape
#     for chapter in chapters:
#         url = build_wuxia_url(title, chapter)
#         # Grab the HTML page
#         wuxia_page = make_GET_request(url)
#         # Soup
#         soup = BeautifulSoup(wuxia_page.content, "html.parser")
#         # Grab chapter_text
#         chapter_text = soup.find_all(dir="ltr")
#         # Grab chapter_title
#         chapter_title = soup.find_all(
#             "h4", 
#             string=lambda text: find_text(text, "Chapter")
#         )[0].text.strip()

#         # Append
#         # chapter_texts.append(chapter_text)
#         # chapter_titles.append(chapter_title)
#         data.append(
#             {
#                 "chapter_title": chapter_title,
#                 "chapter_text": chapter_text
#             }
#         )

#     return data
#     # Generate file
#     # generate_text_file(data, file_name)


# def thread_wuxia(title, chapters, file_name):
#     """
#     Thread scrape_wuxia(title, chapters, file_name). for the amount of chapters
#     """
#     pool = ThreadPool(processes=len(chapters))
    
#     file_data = []
#     requests = []

#     for chapter in chapters:
#         requests.append(pool.apply_async(scrape_wuxia, (title, [chapter])))
#         # target=scrape_wuxia, args=(title, [chapter], f"{file_name}: {chapter}")

#     # Get the data from async
#     for request in requests:
#         file_data.append(request.get())

#     # Flatten file data
#     flat_file_data = [chapter for spec in file_data for chapter in spec]

#     generate_text_file(flat_file_data, file_name)
#     display_txt(f"{file_name}.txt", is_file=True)




if __name__ == "__main__":
    wuxia = WuxiaScraper()
    wuxia.find_novel("Martial God Asura")
    wuxia.download([1])