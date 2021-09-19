from src.backend.utils.clear_scraped import delete_files
from src.backend.data.helper import DOWNLOAD_ID, DOWNLOAD_LOC, DOWNLOAD_SCRAPE_ID, DOWNLOADS_TABLE, DbHelper, SCRAPE_TABLE, SCRAPE_ID
from src.backend.data.models.scrape_model import Scrape


def grab_scrapes():
    """
    Grab the scrapes of the database.

    Returns: <list(Dict)|False>
    """
    db = DbHelper()
    scrapes = db.query_specific(SCRAPE_TABLE)
    db.close_db()
    if not scrapes:
        return False
    return scrapes


def grab_scrape(scrape_id):
    """
    Grab a specific scrape.

    Params:
        - <scrape_id: int> The id of the scrape.

    Returns: <Scrape|False> 
    """
    db = DbHelper()
    scrape = db.query_specific(SCRAPE_TABLE, where=f"{SCRAPE_ID} = {scrape_id}")
    db.close_db()
    # Check not found
    if not scrape:
        return False

    return Scrape.from_sql(scrape)


def add_scrape(scrape: Scrape):
    """
    Add a new scrape.

    Params: 
        - <scrape: Scrape> The scrape to add.
    
    Returns: <int> The scrapes id
    """
    db = DbHelper()
    db.insert(SCRAPE_TABLE, scrape.sql_format())
    # Query scrapes
    scrape = db.query_specific(SCRAPE_TABLE, order=f'BY {SCRAPE_ID} DESC')[0]
    db.close_db()
    # Return id
    return scrape[SCRAPE_ID]
    

def delete_scrape(scrape_id):
    """
    Delete a scrape.

    Params:
        - <scrape_id: int> The id of the scrape to delete.
    """
    db = DbHelper()
    db.delete(SCRAPE_TABLE, scrape_id)
    # Now grab the downloads of the scrape
    downloads = db.query_specific(DOWNLOADS_TABLE, where=f"{DOWNLOAD_SCRAPE_ID} = {scrape_id}")
    # Delete the downloads
    for download in downloads:
        db.delete(DOWNLOADS_TABLE, download[DOWNLOAD_ID])
    db.close_db()

    # Grab files
    files = list(map(lambda d: d[DOWNLOAD_LOC], downloads))
    # Delete
    delete_files(files)