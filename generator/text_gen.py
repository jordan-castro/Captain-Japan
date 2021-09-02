import codecs

def generate_text_file(data, title):
    """
    Generate a text file.

    Params:
        - <data list({'chapter_title': title: str, 'chapter_text': text: str})> the data to put into the file,
        - <title str> name of file
        - <line_len int> how long a line of text should be
    """
    # Variable to write to file
    text = ""

    # Loop through data passed
    for d in data:
        # Data must be list(dict) and meet requirements
        # Contain "chapter_title":str and "chapter_text":list(str) 
        text += f"\n\n\n{d['chapter_title']}\n\n\n"
        # Format chapter_data
        for chd in d['chapter_text']:
            # Textify and strip chapter_text
            chd = chd.text.strip()
            # If last then no break lines
            if chd == d['chapter_text'][-1]:
                text += chd
            else:
                # Otherwise break lines
                text += f"{chd}\n\n"

    # Write file
    with codecs.open(f"{title}.txt", "w", "utf-8") as text_file:
        text_file.write(text)