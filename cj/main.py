from cj.bookmaker import get_chapters_for_maker
from cj.data.cj_db import CJDB
from cj.objects.book import Book
from cj.objects.novel import Novel
from cj.scraper.novels.rnf import RNF
from cj.utils.enums import BookType, CjType
from cj.utils.save import Save
from cj.utils.cmd_args import Args
from cj.bookmaker.epub import EpubMaker
import time

from threading import Thread, current_thread


def scrape_novel(title: str, chapters: list[int]):
    rnf = RNF(title)
    rnf.should_scroll = False
    rnf.should_wait = True
    rnf.wait_time = 1
    # Can not change the data above
    rnf.can_change_scroll = False
    rnf.can_change_wait = False
    # See if the novel exists
    result = rnf.search()
    if result is None:
        return False

    # It's all good let's go
    rnf.load_chapters(result)
    cover = rnf.cover()

    # The novel
    novel = Novel(None, title, None, cover)

    # If no chapters are passed, then we want to scrape ALL of them
    if len(chapters) == 0:
        chapters = [chapter.number for chapter in rnf.chapters]
        
    # Loop through the chapters
    for chapter in chapters:
        # Get the index of ze chapter
        if chapter != 0 and chapter % rnf.limit == 0:
            time.sleep(10)

        novel_chapter = rnf.scrape(rnf.chapters[chapter])
        # Save the chapter asynchronously
        save = Save(novel_chapter, novel)
        Thread(target=save.save).start()

    # We are done with the Scraper
    rnf.quit()
    # Wait for the threads to finish
    current_thread().join()

    print(f"Finished scraping {title}, You might have to wait a moment for all the chapters to show up.")
    print(f"You can find the raw novel in {novel.location}.")


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

    # Now let's get the chapters
    book_chapters = get_chapters_for_maker(chapters, location=location)
    
    book = Book(title)
    book._type = book_type

    # Ard lets make this book
    if book._type == BookType.EPUB:
        maker = EpubMaker(book_chapters, book)
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
    scrape_novel("The beginning after the end", [])
    # create_book_from_novel("The beginning after the end", [
    #     0,1,2,3,4,5,6,7,8,9,10,11,12,13
    # ], BookType.EPUB)