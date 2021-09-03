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


def valid_url(url):
    """
    Check if a url is valid.

    Params:
        - <url: str> the url in question

    Return: <valid: bool>
    """
    try:
        make_GET_request(url)
        return True
    except:
        return False