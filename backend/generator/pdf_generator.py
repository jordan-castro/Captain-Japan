### Script to generate PDF's based off of HTML (LightNovel) or Images (Manga)
import subprocess
import os


def generate_pdf(files, output, novel=True, manga=False):
    """
    Generate a PDF file.

    Params:
        - <files: list(str)> A list of the file paths.
        - <output: str> The name of the PDF, without extension.
        - <novel: bool=True> Default, generate pdf from novel.
        - <manga: bool=False> Default, generate pdf from manga

    Returns <str>
    """
    # Create data file in .txt format
    with open("pdf-data.txt", 'w') as data_file:
        # Add the pdf title as the first line
        data_file.write(f"{output}\n")
        for file in files:
            data_file.write(f"{file}\n")
    
    pdf_data_file = os.getcwd() + "/pdf-data.txt"
    # Now call the execution script
    subprocess.call(f'cd converter/pdf && htmltopdf {pdf_data_file}', shell=True)