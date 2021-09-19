from src.backend.converter.epub import Epub


def generate_epub(downloads, output):
    """
    Generate a epub based on the HTML files passed.

    Params:
        - <downloads: List(Download)> A list of downloads.
        - <output: str> The name of the EPUB.

    Returns: <str> The path to epub.
    """
    epub = Epub(output, 'en', 'CaptainJapan')
    # Loop through files and add to epub
    for download in downloads:
        epub.add_chapter(download.location, download.name)
    
    # Now build the EPUB
    epub.build_epub()

    return epub.path