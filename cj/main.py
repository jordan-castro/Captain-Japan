from cj.bookmaker import get_chapters_for_maker
from cj.bookmaker.pdf import PdfMaker
from cj.crawler.crawl import Crawler
from cj.data.cj_db import CJDB
from cj.objects.book import Book
from cj.objects.chapter import Chapter
from cj.objects.novel import Novel
from cj.scraper.novels.ltn import LTN
from cj.scraper.novels.rnf import RNF
from cj.utils.enums import BookType, CjType
from cj.utils.cmd_args import Args
from cj.bookmaker.epub import EpubMaker


def scrape_novel(title: str, chapters: list[int], source: str, url: str):
    if source == 'rnf':
        scraper = RNF(title, url)
        # Set the data
        scraper.should_scroll = False
        scraper.should_wait = True
        scraper.wait_time = 1
        # Can not change data above
        scraper.can_change_scroll = False
        scraper.can_change_wait = False
        time_between_scrape = 60
    elif source == 'ltn':
        scraper = LTN(title, url)
        # Set the data
        s_chapters = [
            Chapter(None, None, f"Chapter {i + 1}") for i in chapters
        ]
        scraper.chapters = s_chapters
        time_between_scrape = 0
    # Start the crawler obejct
    crawler = Crawler(scraper, CjType.NOVEL, time_between_scrape)
    
    # Try and crawl
    try:
        crawler.crawl(chapters)
    except Exception as e:
        print(f"Something went wrong with crawling: {e}")


def create_book_from_novel(title, chapters, book_type):
    # Check if the Novel exists in the DB
    cj_db = CJDB()
    novel = cj_db.search_title(title, CjType.NOVEL)
    if not novel:
        return False
    # The novel does exists, convert Dict to novel object
    novel = Novel.from_json(novel[0])
    # Get the location
    location = novel.location

    _type = "txt" if book_type == BookType.PDF else "html"
    # Now let's get the chapters
    book_chapters = get_chapters_for_maker(chapters, location=location, type=_type)
    
    book = Book(title)
    book._type = book_type

    # Ard lets make this book
    if book._type == BookType.EPUB:
        maker = EpubMaker(book_chapters, book)
    elif book._type == BookType.PDF:
        maker = PdfMaker(book_chapters, book)
    else:
        raise NotImplementedError

    try:
        # Make that shit
        maker.setup("English")
        maker.make()
        print(f"Book {book.title} has been made!")
        print(f"You can find it at {maker.path}")
    except Exception as e:
        print(f"Something went wrong with making the book: {e}")


if __name__ == "__main__":
    chapters = [c for c in range(0, 14)]

    # scrape_novel("Mushoku Tensei Jobless Oblige", chapters, "ltn") # Scrape example
    create_book_from_novel("Mushoku Tensei Jobless Oblige", chapters, BookType.EPUB) # Convert into ebook example