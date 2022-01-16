class NoJsException(Exception):
    # This is an exception for when the scraper cannot find the javascript element.
    def __init__(self):
        super().__init__("JavaScript is not enabled.")


class NoSoupException(Exception):
    # This is an exception for when the scraper cannot find the soup element.
    def __init__(self):
        super().__init__("Cannot create a BeautifulSoup object.")


class NoScrollException(Exception):
    # This is an exception for when the Scrapper class has should_scroll set to False
    def __init__(self):
        super().__init__("self.should_scroll is False")


class NoEmailException(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)


class IncorrectFormatException(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)