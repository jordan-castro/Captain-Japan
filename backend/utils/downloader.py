### Script to handle the downloads and generations.
from backend.data.models.download_model import Download
from multiprocessing.pool import ThreadPool
from backend.generator.html_gen import generate_html_file
from backend.generator.generate_manga import generate_manga
from backend.utils.default_title import default_title


def download_novel(novel_title, chapters, scrape_method, async_=True):
    """
    Download a novel.

    Params:
        - <novel_title: str> The title of the novel to download.
        - <chapters: list(int)> The chapters to download.
        - <scrape_method: def> The method that will scrape the data
        - <async_: bool=True> Should we run this method asynchronously?

    Return: <list(Download)>
    """
    downloads = []
    # Title of novel universal
    title = default_title(novel_title)
    if async_:
        # Pool for quicker speed
        pool = ThreadPool(processes=len(chapters))

        # Requests
        reqs = []


        # Start the process for reading chapter data
        for chapter in chapters:    
            reqs.append(pool.apply_async(scrape_method, (chapter, )))

        # Now grab the data
        for req in reqs:
            # Data
            chapter_data = req.get()
            # Verify data
            if not chapter_data:
                continue

            # Name of file
            file_name = f"Chapter_{chapters[reqs.index(req)]}"
            # Write file
            file_path = generate_html_file(chapter_data, file_name, directory=title)
            downloads.append(
                Download(
                    title=title,
                    name=file_name,
                    location=file_path,
                    image=None,
                    download_type=1,
                )
            )
    else:
        # For synchronous calls. Required when webpage needs to run javascript
        for chapter in chapters:
            # Grab data
            chapter_data = scrape_method(chapter)
            file_name = f"Chapter_{chapter}"
            file_path = generate_html_file(chapter_data, file_name, directory=title)
            # Add to downloads
            downloads.append(
                Download(
                    title=title,
                    name=file_name,
                    location=file_path,
                    image=None,
                    download_type=1
                )
            )

    # Now return download data
    return downloads


def download_manga(manga_title, chapters, scraper):
    """
    Download Manga.

    Params:
        - <manga_title: str> The title of the manga.
        - <chapters: list(int)> The chapters to download.
        - <scraper: Object> The scraper object.

    Return: <list(Download)>
    """
    # Thread to save time
    pool = ThreadPool(processes=len(chapters))

    reqs = []
    title = default_title(manga_title)

    # Request data
    for chapter in chapters:
        # Change to correct chapter
        scraper.browser.change_page(scraper.build_url(chapter))
        # Apply the request
        reqs.append(pool.apply_async(scraper.scrape, (chapter, scraper.browser.get_page())))

    for req in reqs:
        # Data from req
        chapter_data = req.get()
        # Verify
        if not chapter_data:
            continue

        # Generate manga files
        paths = generate_manga(chapter_data, title)

    # Verify content
    if not paths:
        return
    
    return list(
        map(
            lambda path: Download(
                title=title,
                name=path.split('/')[-1].replace('.png', ''),
                location=path,
                image=None,
                download_type=2
            ),
            paths
        )
    )