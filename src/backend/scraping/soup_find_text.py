# Script to return the correct text rather than False or None when using BeautifulSoup

def find_text(text, find):
    if not text:
        return None
    else:
        return find in text