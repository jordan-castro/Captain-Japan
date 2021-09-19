# Script to generate PDF's based off of HTML (LightNovel) or Images (Manga)
from src.backend.converter.pdf import PDF, NOVEL_PDF, MANGA_PDF


def generate_pdf(files, output, novel=False, manga=False):
    """
    Generate a PDF file.

    Params:
        - <files: list(str)> A list of the file paths.
        - <output: str> The name of the PDF, without extension.
        - <novel: bool=True> Default, generate pdf from novel.
        - <manga: bool=False> Default, generate pdf from manga

    Returns <str>
    """
    if novel:
        pdf_type = NOVEL_PDF
    elif manga:
        pdf_type = MANGA_PDF
    else:
        # BAKA! You can only have novel or manga!
        return

    # Start the PDF object
    pdf = PDF(output, pdf_type)

    # Loop through files passed and add them to the pdf
    for f in files:
        if novel:
            pdf.add_html(f)
        else:
            pdf.add_image(f)

    # Now le'ts build the PDF
    path = pdf.build()
    return path