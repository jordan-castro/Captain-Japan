# Script to handle the downloads and generations.
from backend.scraping.scraper_base import Scraper
from backend.data.models.download_model import Download
from multiprocessing.pool import ThreadPool
from backend.generator.html_gen import generate_html_file
from backend.generator.generate_manga import generate_manga
from backend.utils.default_title import default_title


class Downloader:
    """
    Handle all downloads from scraping and such.
    """

    def download(self, title: str, chapters: list, scraper: Scraper, t: int, async_=True):
        """
        Download the scraped source from the internet.

        Params:
            - <title: str> The title of the novel/manga/anime.
            - <chapters: list(int)> a list of integers.
            - <scraper: Scraper> a scraper object.
            - <t: int> The type or scraping being done. Novel,Manga,Anime
            - <async_: bool=True> Whether or not we should run this asynchronoulsy. Default is true.

        Returns: <list(Download)>
        """
        self.scraper = scraper
        self.t = t

        downloads = []
        title = default_title(title)

        if async_:
            data = self.__download_async(chapters)
        else:
            data = self.__download_sync(chapters)

        # Now do the download
        for chp in data:
            # File name
            if "chapter_title" in chp:
                file_name = chp["chapter_title"]
            else:
                file_name = f"Chapter_{data[data.index(chp)]}"

            if self.t == 0:
                # Add a download
                download = generate_html_file(chp, file_name, title)
                downloads.append(
                    Download(
                        name=file_name,
                        location=download,
                        user_id=1
                    )
                )
            elif self.t == 1:
                # Add the downloads
                download = generate_manga(chp, title)
                map(
                    lambda path: downloads.append(
                        Download(
                            name=file_name,
                            location=path,
                            user_id=1
                        )
                    ),
                    download
                )

        return downloads

    def __download_async(self, chapters):
        pool = ThreadPool(processes=len(chapters))
        # Hold the requests
        reqs = []
        # Hold the chapter data
        _chapters = []
        # Loop through chapters
        for chapter in chapters:
            # Apply asynchronus
            if self.t == 0:
                a = pool.apply_async(self.scraper.scrape, (chapter, ))
            elif self.t == 1:
                self.scraper.change_page(self.scraper.build_url(chapter))
                a = pool.apply_async(
                    self.scraper.scrape,
                    (
                        chapter, self.scraper.get_page()
                    )
                )

            # Add to requests
            reqs.append(a)

        for req in reqs:
            # Grab data
            data = req.get()
            # Check compiler suggestions
            if not data:
                continue

            _chapters.append(data)

        return _chapters

    def __download_sync(self, chapters):
        # Hold the chapter_data
        _chapters = []
        for chapter in chapters:
            if self.t == 0:
                data = self.scraper.scrape(chapter)
            elif self.t == 1:
                self.scraper.change_page(self.scraper.build_url(chapter))
                data = self.scraper.scrape(chapter, self.scraper.get_page())

            _chapters.append(data)

        return _chapters
