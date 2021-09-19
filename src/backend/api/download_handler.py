# Api to handle downloads
from src.backend.utils.downloader import Downloader
from src.backend.scraping.novel_src.wuxia_world import WuxiaScraper
from src.backend.scraping.novel_src.light_novel_pub import LightNovelPub
from src.backend.scraping.novel_src.novel_full import ReadNovelFull
from src.backend.scraping.manga_src.manga_kakalot import MangaKakalot
from src.backend.data.helper import DOWNLOAD_ID, DOWNLOAD_SCRAPE_ID, DOWNLOADS_TABLE, DbHelper


def handle_download(title: str, type: int, d_range: list, source: str, scraped_id: int, blacklist=[]):
    """
    Handle the downloads from the API.

    Params:
        - <title: str> The title of the download.
        - <type: int> The type of download. IE. Manga, LN, Anime
        - <d_range: list(int)> The start and end of the chapters|Episodes
        - <source: str> The source to download from.
        - <scraped_id: int> The id of the scraping.
        - <blacklist: list(int)=[]> Which chapters|Episodes should we black list if any.
    
    Returns: <list(Download)> a list of downloads.
    """
    scraper = None
    db = DbHelper()
    downloads = []
    async_ = True

    if type == 0:
        # Check sources
        if source.lower() == 'ww':
            # Download for wuxia world
            scraper = WuxiaScraper()
        elif source.lower() == 'lnp':
            scraper = LightNovelPub()
            async_ = False
        elif source.lower() == "rnf":
            scraper = ReadNovelFull()
        else:
            # BAKA! We only have these ^ sources available RN!
            return []
    elif type == 1:
        # Manga stuff
        if source.lower() == 'mka':
            scraper = MangaKakalot()
            async_ = False
        else:
            # BAKA! We only have these ^ sources available RN!
            return []
    else:
        # BAKA! Anime scraping not implemented yet.
        return []


    # Do the scraping
    hit = scraper.find(title)
    # Check if not hit
    if not hit:
        # BAKA! Something went wrong
        return []
    # Set chapters to download
    chapters = []
    for x in d_range:
        if x in blacklist:
            continue
        chapters.append(x)
    
    # Do the actual downloading
    downloader = Downloader()
    _downloads = downloader.download(title, chapters, scraper, type, async_=async_)

    # Save the downloads
    for download in _downloads:
        db.insert(DOWNLOADS_TABLE, download.sql_format(scraped_id))

    # Grab the downloads from the database
    downloads = db.query_specific(DOWNLOADS_TABLE, where=f"{DOWNLOAD_SCRAPE_ID} = {scraped_id}")

    # Close database and return downloads
    db.close_db()
    return downloads


def grab_scrape_downloads(scrape_id):
    """
    Grab the downloads of a specific scrape based on it's id.

    Params:
        - <scrape_id: int> The id of the scrape.

    Returns: <list(dict)|False>
    """
    db = DbHelper()
    # 0 is a universal grab for all
    if scrape_id > 0:
        downloads = db.query_specific(DOWNLOADS_TABLE, where=f"{DOWNLOAD_SCRAPE_ID} = {scrape_id}", order=f"BY {DOWNLOAD_ID} DESC")
    else:
        downloads = db.query_downloads()
    db.close_db()
    
    return downloads
