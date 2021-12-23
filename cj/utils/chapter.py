class Chapter(object):
    """
    A object to hold chapter info.

    Params:
        - url(str): The url to the chapter destination.
        - number(int): The chapter number, not always available.
        - title(str): The chapter title, not always available.
    """
    url: str = None
    number: int = None
    title: str = None

    def __init__(self, url: str=None, number: int=None, title: str=None):
        self.url = url
        self.number = number
        self.title = title
    
    def __str__(self):
        return f"Chapter {self.number}: {self.title} ({self.url})"

    def __repr__(self):
        return f"Chapter({self.url}, {self.number}, {self.title})"

    def __eq__(self, other):
        return self.url == other.url and self.number == other.number and self.title == other.title

    def __hash__(self):
        return hash((self.url, self.number, self.title))
