from backend.data.dir import manga_dir, novels_dir
import subprocess
import os
from pathlib import Path
from glob import glob
import codecs


NOVEL_PDF = 0
MANGA_PDF = 1


class PDF:
    def __init__(self, pdf_name, pdf_type):
        self.name = pdf_name
        
        if pdf_type == NOVEL_PDF:
            self.path = novels_dir() + self.name + "-pdf"
        elif pdf_type == MANGA_PDF:
            self.path = manga_dir() + self.name + "-pdf"

        self.files = glob(f"{self.path}/*.html")

        # Check if the path to the PDF exists or not
        if not Path(self.path).exists():
            # Create it
            os.mkdir(self.path)

    def add_html(self, html_path):
        """
        Add a html file to the PDF. Used for novels.

        Params:
            - <html_path: str> The path to the HTML file
        """
        # Add html_data to a new file within PDF directory
        html_data = ""
        with codecs.open(html_path, "r", "utf-8") as html_file:
            html_data = html_file.read()

        # Write to new file
        new_file_path = self.path + f"/{len(self.files)}_.html"
        with codecs.open(new_file_path, 'w', 'utf-8') as new_file:
            for data in html_data:
                new_file.write(data)

        # Add new file path to self.files
        self.files.append(new_file_path)

    def add_image(self, image_path):
        """
        Add a Image to the PDF. Used for Manga.

        Params:
            - <image_path: str> The path to the Image file.
        """
    
    def build(self):
        """
        Build the PDF.

        Returns: <pdf_path: str>
        """
        # Check if we have more than one file
        if len(self.files) > 1:
            self.__combine_files()
        
        finished_pdf_path = f"{self.path}/{self.name}.pdf"

        command = f"wkhtmltopdf {self.path}/pdf.html {finished_pdf_path}"
        subprocess.call(command, shell=True)

        # Now remove the pdf.html
        os.unlink(f"{self.path}/pdf.html")

        return finished_pdf_path

    def __combine_files(self):
        """
        Combine the files into one file. 
        """
        # Open the file to write to
        with codecs.open(self.path + "/pdf.html", 'w', 'utf-8') as pdf_html:
            # Let's loop through the current files
            for f in self.files:
                with codecs.open(f, 'r', 'utf-8') as html:
                    # Write to the pdf_html
                    pdf_html.write(html.read())
                # Now delete the file
                os.unlink(f)
            # Daijobu!