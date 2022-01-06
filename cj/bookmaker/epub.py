from ebooklib import epub
from cj.bookmaker import BookMaker, Book
from cj.bookmaker.add_title import add_title


class EpubMaker(BookMaker):
    epub_book: epub.EpubBook = None

    def __init__(self, chapters: list[str], book: Book, description: str = None) -> None:
        super().__init__(chapters, book, description=description)

    def setup(self, language, cover=None):
        """
        Setup the epub_book.

        Params:
            - <language: str> The language of the book.
            - <cover: bytes> The path to the cover.
        """
        self.epub_book = epub.EpubBook()
        self.epub_book.set_identifier(self.book.title)
        self.epub_book.set_title(self.book.title)
        self.epub_book.set_language(language)

        # Add description
        self.epub_book.add_metadata('DC', 'description', self.description)

        if cover is not None:
            # Add cover
            self.epub_book.set_cover("cover", cover)
        self._add_chapters()

    def _add_chapters(self):
        """
        Add the chapters to the epub.
        """
        # Loop through the chapters and reformat them
        for chapter in self.chapters:
            # The xml path
            xml_path = f"{self.chapters.index(chapter)}.xhtml"
            # The title of the chapter
            title = "Chapter " + str(self.chapters.index(chapter) + 1)
            epub_chapter = epub.EpubHtml(
                title=title,
                file_name=xml_path
            )

            # Add the title to the chapter
            content = add_title(chapter)

            # Add content to chapter
            epub_chapter.set_content(content)

            # Add chapter to epub
            self.epub_book.add_item(epub_chapter)
            # Add chapter to formatted chapters
            self.formatted_chapters.append(epub_chapter)

    def make(self):
        """
        Make the book.
        """
        # The table of contents
        toc = []
        # Add the chapters to the table of contents
        for chapter in self.formatted_chapters:
            toc.append(
                epub.Link(
                    chapter.file_name,
                    chapter.title,
                    chapter.id
                )
            )

        # Now convert the toc to tuple
        toc = tuple(toc)
        spine = self.formatted_chapters
        ncx = epub.EpubNcx()
        nav = epub.EpubNav()

        # Set needed stuff for epub
        self.epub_book.toc = toc
        self.epub_book.spine = spine
        self.epub_book.add_item(ncx)
        self.epub_book.add_item(nav)

        # Now write the epub
        epub.write_epub(self.path, self.epub_book)

        # Save the book to the database
        self.save()