import codecs
from pathlib import Path
from os import mkdir
from backend.data.dir import novels_dir


def generate_text_file(data, title, directory):
    """
    Generate a text file.

    Params:
        - <data list({'chapter_title': title: str, 'chapter_text': text: str})> the data to put into the file,
        - <title str> name of file
        - <line_len int> how long a line of text should be

    Returns: <str> file path
    """
    # Variable to write to file
    text = ""

    # Data must be list(dict) and meet requirements
    # Format chapter_data
    for chd in data['chapter_text']:
        # Textify and strip chapter_text
        chd = chd.text.strip()
        # If last then no break lines
        if chd == data['chapter_text'][-1]:
            text += chd
        else:
            # Otherwise break lines
            text += f"{chd}\n\n"

    path_to_dir = f"{novels_dir()}{directory}"

    # Check if directory does not exists And if not then create it
    if not Path(path_to_dir).exists():
        mkdir(path_to_dir)

    file_path = f"{path_to_dir}/{title}.txt"

    # Write file
    with codecs.open(file_path, "w", "utf-8") as text_file:
        text_file.write(text)

    return file_path