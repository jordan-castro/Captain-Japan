from generator.text_gen import generate_text_file
from scraping.req import make_GET_request
from bs4 import BeautifulSoup
from display.text import display_txt
from scraping.soup_find_text import find_text
from multiprocessing.pool import ThreadPool


def build_wuxia_url(title, chapter):
    """
    Build a WuxiaWorld URL based on the title and chapter.

    Params:
        - <title: str> the title of the series.
        - <chapter: int> the chapter to grab.

    Return: <url: str>
    """
    return f"https://www.wuxiaworld.com/novel/{title.replace(' ', '-').lower()}/necro-chapter-{chapter}"


def thread_wuxia(title, chapters, file_name):
    """
    Thread scrape_wuxia(title, chapters, file_name). for the amount of chapters
    """
    pool = ThreadPool(processes=len(chapters))
    
    file_data = []
    requests = []

    for chapter in chapters:
        requests.append(pool.apply_async(scrape_wuxia, (title, [chapter])))
        # target=scrape_wuxia, args=(title, [chapter], f"{file_name}: {chapter}")

    # Get the data from async
    for request in requests:
        file_data.append(request.get())

    # Flatten file data
    flat_file_data = [chapter for spec in file_data for chapter in spec]

    generate_text_file(flat_file_data, file_name)
    display_txt(f"{file_name}.txt", is_file=True)


def scrape_wuxia(title, chapters):
    """
    Scrape the Wuxia World website based on the title of the series and chapter numbers.

    Params:
        - <title: str> The title of the series
        - <chapters: list|int> A list of chapter numbers or one chapter

    Return: <success: bool>
    """
    # Data to send to generator
    data = []

    # Scrape
    for chapter in chapters:
        url = build_wuxia_url(title, chapter)
        # Grab the HTML page
        wuxia_page = make_GET_request(url)
        # Soup
        soup = BeautifulSoup(wuxia_page.content, "html.parser")
        # Grab chapter_text
        chapter_text = soup.find_all(dir="ltr")
        # Grab chapter_title
        chapter_title = soup.find_all(
            "h4", 
            string=lambda text: find_text(text)
        )[0].text.strip()

        # Append
        # chapter_texts.append(chapter_text)
        # chapter_titles.append(chapter_title)
        data.append(
            {
                "chapter_title": chapter_title,
                "chapter_text": chapter_text
            }
        )

    return data
    # Generate file
    # generate_text_file(data, file_name)


if __name__ == "__main__":
    chapters = []
    for x in range(100):
        chapters.append(x + 1)    
    thread_wuxia("Necropolis Immortal", chapters, "My man")