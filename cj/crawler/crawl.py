from cj.objects.chapter import Chapter
from cj.objects.novel import Novel
from cj.scraper.novel_base import NovelBase
from cj.utils.enums import CjType
from threading import Thread

import time

from cj.utils.save import Save


class Crawler:
    """
    This class handles the calling of the scraper.
    """
    
    def __init__(self, source, cj_type: CjType, time_between_scrape: int = 10) -> None:
        self.source = source
        self.type = cj_type
        self.time_between_scrape = time_between_scrape

    def crawl(self, chapters: list[int]) -> None:
        """
        Crawl the chapters passed.
        """
        if self.type == CjType.MANGA:
            pass
        elif self.type == CjType.NOVEL:
            # Set the Base class
            self.source: NovelBase = self.source
            novel: Novel = Novel(None, self.source.title, None, None)
            # Load the chapters
            self.source.load_chapters(self.source.base_url)
            for i in chapters:
                # Grab the chapter based on index
                chapter = self.source.chapters[i]
                if chapter.number is None:
                    chapter.number = i
                chapter = self.source.scrape(chapter)
                # Save the chapter assynchronously
                save = Save(chapter, novel)
                Thread(target=save.save).start()
                # Wait the time_between_scrape
                time.sleep(self.time_between_scrape)
            # Quit the scraper and join the current thread
            self.source.quit()

            # Some CMD L
            print(f"Finished scraping {self.source.title}, You can find the source in {novel.location}.")

        else:
            raise NotImplementedError("Anime is not yet supported.")
