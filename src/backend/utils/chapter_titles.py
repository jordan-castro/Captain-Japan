### Script to clean the titles of chapters/episodes

def clean_title(title: str):
    # First remove that weird ’
    cleaned = title.replace('’', "'")
    print(cleaned)
    return cleaned