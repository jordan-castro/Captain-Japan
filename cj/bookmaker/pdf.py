from cj.bookmaker import BookMaker, Book
import subprocess


# The path to the pdf_maker executable
PDF_MAKER_LOCATION = "extensions/pdf/pdf_maker.exe"


class PdfMaker(BookMaker):
    def __init__(self, chapters: list[str], book: Book, description: str = None) -> None:
        super().__init__(chapters, book, description=description)

    def setup(self, language, cover=None):
        pass        

    def make(self):
        # Convert the list of strings into a single string, joined by ';'
        chapters = ";".join(self.chapters)
        chapters += f";{self.path}"

        # Call the pdf_maker executable
        subprocess.call([PDF_MAKER_LOCATION, chapters])
        # Save to the database.
        # self.save()

if __name__ == "__main__":
    pass