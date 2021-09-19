import requests


def make_GET_request(url, headers=None):
    """
    Make a GET request to <url> and get back the HTML page content.

    Params:
        - <url: str> the url
        - <headers: dict> custom headers
    
    Return: <html_page: Response>
    """
    page = requests.get(url, headers=headers)
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


def valid_image_url(url):
    """
    Validate that a url contains the correct headers.

    Params:
        - <url: str> the url to validate.
        - <headers: tuple(str)> headers

    Return: <bool>
    """
    image_formats = ("image/png", "image/jpeg", "image/gif")

    # Grab url headers
    headers_from_url = requests.get(url)
    print(headers_from_url.headers)
    # Check
    if headers_from_url.headers['content-type'] in image_formats:
        return True
    else:
        return False