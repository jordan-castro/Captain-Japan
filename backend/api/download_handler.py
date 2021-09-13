# Api to handle downloads
from backend.utils.downloader import download_manga, download_novel
from backend.api.sources import LIGHT_NOVEL_PUB, MANGA_KAKALOT, WUXIA_WORLD
from backend.scraping.novel_src.wuxia_world import WuxiaScraper
from backend.scraping.novel_src.light_novel_pub import LightNovelPub
from backend.scraping.manga_src.manga_kakalot import MangaKakalot
from backend.data.helper import DOWNLOAD_SCRAPE_ID, DOWNLOADS_TABLE, DbHelper


def handle_download(title: str, type: int, d_range: list, source: str, scraped_id: int,blacklist=[]):
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

    if type == 0:
        # Check sources
        if source == WUXIA_WORLD:
            # Download for wuxia world
            scraper = WuxiaScraper()
            async_ = False
        elif source == LIGHT_NOVEL_PUB:
            scraper = LightNovelPub()
            async_ = True
        else:
            # BAKA! We only have these ^ sources available RN!
            return []
    elif type == 1:
        # Manga stuff
        if source == MANGA_KAKALOT:
            scraper = MangaKakalot()
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
    if type == 0:
        _downloads = download_novel(scraper.novel_title, chapters, scraper.scrape, async_=async_)
    elif type == 1:
        _downloads = download_manga(scraper.manga_title, chapters, scraper)
    else:
        # BAKA! No anime source yet. COMING SOON! CHOTO MATE!
        return []

    # Save the downloads
    for download in _downloads:
        db.insert(DOWNLOADS_TABLE, download.sql_format(scraped_id))

    # Grab the downloads from the database
    downloads = db.query_specific(DOWNLOADS_TABLE, where=f"{DOWNLOAD_SCRAPE_ID} = {scraped_id}")

    # Close database and return downloads
    db.close_db()
    return downloads