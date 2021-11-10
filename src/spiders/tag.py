from selenium.webdriver.common.by import By


class Tag(object):
    """
    Oject to hold the tag data for a scraper.

    Properties:
        tag_type: By
            The tage type, whether its a class, id, name, or x-path
        tag_value: str
            The value of the tag.
    """
    def __init__(self, tag_type: By, tag_value: str) -> None:
        self.tag_type = tag_type
        self.tag_value = tag_value        
        super().__init__()