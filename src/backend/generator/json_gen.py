import json
import codecs


def generate_json_file(data, output):
    """
    Generate a JSON file based on the data passed.

    Important: data should not be json yet.

    Params:
        - <data: list(dict)> data to turn into json
        - <output: str> the output file name
    """

    data = list(map(lambda chapter_data: clean_data(chapter_data), data))

    with codecs.open(f"{output}.json", "w", "utf-8") as json_file:
        json_file.write(json.dumps(data))


def clean_data(data):
    cleaned_text = []
    # Grab chapter text
    chapter_text = data['chapter_text']
    for text in chapter_text:
        # Stip text
        striped = text.text.strip()
        if text == chapter_text[-1]:
            text = striped
        else:
            text = f"{striped}\n\n"
        # Add the now cleaned text
        cleaned_text.append(text)
    
    # Implode cleaned_text
    return {
        "title": data['chapter_title'],
        "body": " ".join(cleaned_text)
    }