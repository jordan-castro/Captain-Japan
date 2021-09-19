from src.backend.data.dir import manga_dir, novels_dir
import subprocess
import os
from pathlib import Path
import codecs
from PIL import Image


NOVEL_PDF = 0
MANGA_PDF = 1


class PDF:
    def __init__(self, pdf_name, pdf_type):
        self.name = pdf_name
        
        if pdf_type == NOVEL_PDF:
            self.path = novels_dir(True) + self.name
        elif pdf_type == MANGA_PDF:
            self.path = manga_dir(True) + self.name
            # Let the class know we are generating MANGA PDF
            self.manga = True

        self.files = []

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
        # Just add the image
        self.files.append(image_path)
    
    def build(self):
        """
        Build the PDF.

        Returns: <pdf_path: str>
        """
        finished_pdf_path = f"{self.path}/{self.name}.pdf"
        
        # Check if we are building Manga or Novel
        if not self.manga:
            # Check if we have more than one file
            if len(self.files) > 1:
                self.__combine_files()
        
            command = f"wkhtmltopdf {self.path}/pdf.html {finished_pdf_path}"
            subprocess.call(command, shell=True)
        else:
            # Generating Manga
            images = []
            # Loop through the images
            for file in self.files:
                img = Image.open(file)
                img = img.convert('RGB')
                images.append(img)
            # Now save the images
            manga_image = images[0]
            manga_image.save(finished_pdf_path, save_all=True, append_images=images)

        # And delete everything other than the .pdf
        for file in os.listdir(self.path):
            if not file is f"{self.name}.pdf":
                os.unlink(file)

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