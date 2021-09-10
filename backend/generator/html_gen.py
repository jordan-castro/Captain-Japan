from backend.utils.dir_helper import hide_dir
from pathlib import Path
from os import mkdir
from backend.data.dir import novels_dir


def generate_html_file(data, title, directory):
    """
    Generate a HTML file that can later be parsed to PDF-EPUB and so on.

    Params:
        - <data: list({'chapter_title': title: str, 'chapter_text': text: str})> the data to put into the file,
        - <title: str> name of file
        - <directory: str> the name of the directory
    
    Returns: <str> file path
    """
    # Grab the path to the directory
    path_to = f"{novels_dir()}{directory}"

    # Check does not exists
    if not Path(path_to).exists():
        mkdir(path_to)
        # And hide
        hide_dir(path_to)

    file_path = f"{path_to}/{title}.html"

    # Create file
    with open(file_path, "w", encoding="utf-8") as html_file:
        # First write the <meta> needed for converting to PDF
        html_file.write('<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">\n')
        html_file.write(f'<h1>{title.replace("_", " ")}</h1>')
        # Write the html
        for html in data['chapter_text']:
            html_file.write(str(html))

    return file_path