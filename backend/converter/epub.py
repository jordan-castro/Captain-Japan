# Script to convert LightNovels to EPUB
from backend.utils.dir_helper import create_if_missing
from backend.data.dir import novels_dir
from ebooklib import epub
import codecs


class Epub:
    def __init__(self, title, language, author, description=None):
        self.title = title
        self.language = language
        self.author = author
        self.id = f"{self.title}-{len(self.title)}"
        self.description = description or f"Epub version of {title}"
        self.chapters = []

        # Set in self.__setup()
        self.book = None

        # Set in self.add_intro()
        self.intro = None

        self.path = novels_dir() + f"{self.title}/" + self.id + ".epub"
        create_if_missing(novels_dir() + self.title)

        # Setup the book
        self.__setup()

    def __setup(self):
        """
        Setup the EPUB book.
        """
        book = epub.EpubBook()
        # Setup for EPUB
        book.set_identifier(self.id)
        book.set_title(self.title)
        book.set_language(self.language)

        # Add description
        book.add_metadata('DC', 'description', self.description)
        # Now set the book
        self.book = book

    def add_chapter(self, html_path, title):
        """
        Add a chapter to EPUB. Important, must be HTML.

        Params:
            - <html_path: str> The path to the html file.
            - <title: str> The chapter title.
        """
        chapter_path = f"{title}_{len(self.chapters)}.xhtml"

        chapter = epub.EpubHtml(
            title=title,
            file_name=chapter_path
        )
        # Add content to chapter
        with codecs.open(html_path, 'r', 'utf-8') as html_file:
            chapter.set_content(html_file.read())

        # Add chapter to self.chapthers
        self.chapters.append(chapter)
        # Now add chapter to book
        self.book.add_item(chapter)

    def add_intro(self, html_path):
        """
        Add a intro chapter to the EPUB. Important, must be HTML file.
        Can only have one intro.

        Params:
            - <html_path: str> The path to the HTML file.
        """
        if self.intro:
            # BAKA! You can only have one intro.
            return

        intro = epub.EpubHtml(
            title="Introduction",
            file_name="intro.xhtml",
        )
        # Add content
        with codecs.open(html_path, 'r', 'utf-8') as html_file:
            intro.set_content(html_file.read())
        # Thats it, YOKONAI!

    def build_epub(self):
        """
        Build the EPUB.
        """
        # Do table of contents
        toc = []
        if self.intro:
            # Add intro to table of contents
            toc.append(
                epub.Link(
                    self.intro.file_name,
                    self.intro.title,
                    self.intro.id
                )
            )
        # Now add the chapters (Kinda sorta)
        chapters = [
            epub.Section("Hombre"),
            self.chapters
        ]
        toc.append(chapters)

        # Now add to the Tupple
        toc = tuple([tuple(t) for t in toc])
        spine = self.chapters
        ncx = epub.EpubNcx()
        nav = epub.EpubNav()

        # Set all the needed stuff for the EPUB
        self.book.toc = toc
        self.book.spine = spine
        self.book.add_item(ncx)
        self.book.add_item(nav)
        # Now write the epub
        print(self.path)
        epub.write_epub(self.path, self.book)