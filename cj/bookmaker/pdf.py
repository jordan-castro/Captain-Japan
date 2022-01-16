from bcrypt import os
from cj.bookmaker import BookMaker, Book
import subprocess
import json

from cj.utils.naming import get_file_name


# The path to the pdf_maker executable
PDF_MAKER_LOCATION = "extensions/pdf/pdf_maker.exe"


class PdfMaker(BookMaker):
    def __init__(self, chapters: list[str], book: Book, description: str = None) -> None:
        super().__init__(chapters, book, description=description)

    def setup(self, language, cover=None):
        # ! PDF Maker does not support language or cover so we just pass this method.
        pass

    def format_chapters(self) -> list:
        """
        Format the chapters to either match a Manga or a Novel.
        """
        if self.book.is_manga:
            chapters = []
            for chapter in self.chapters:
                chapters.append({
                    "title": get_file_name(chapter),
                    "pages": [

                    ]
                })
            return chapters
        else:
            return self.chapters

    def make(self):
        # TODO The PDF_Maker executable has changed logic, to accept a JSON file as input.
        # Write to a Json file with the pdf data
        pdf_json = {
            "title": self.book.title,
            "author": "Captain Japan", # TODO: Add author
            "isManga": self.book.is_manga,
            "output": self.path,
            "chapters": self.format_chapters(),
        }
        with open("pdf.json", "w") as f:
            f.write(json.dumps(pdf_json))

        # Run the PDF_Maker executable
        subprocess.run([PDF_MAKER_LOCATION, "pdf.json"])
        # delete the json file
        os.remove("pdf.json")
        # Save to the database.
        self.save()

if __name__ == "__main__":
    pass