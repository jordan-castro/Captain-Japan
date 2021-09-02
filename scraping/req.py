import requests


def make_GET_request(url):
    """
    Make a GET request to <url> and get back the HTML page content.

    Params:
        - <url: str> the url
    
    Return: <html_page: Response>
    """
    page = requests.get(url)
    return page