from backend.converter.epub import Epub


def generate_epub(files, output):
    """
    Generate a epub based on the HTML files passed.

    Params:
        - <files: list(str)> List of HTML file paths.
        - <output: str> The name of the EPUB.

    Returns: <str> The path to epub.
    """
    epub = Epub(output, 'en', 'CaptainJapan')
    # Loop through files and add to epub
    for f in files:
        chapter_title = f"Chapter {files.index(f)}"
        epub.add_chapter(f, chapter_title)
    
    # Now build the EPUB
    epub.build_epub()

    return epub.path