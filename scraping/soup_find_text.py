# Script to return the correct text rather than False or None when using BeautifulSoup

def find_text(text):
    if not text:
        return None
    else:
        return "Chapter" in text