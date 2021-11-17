from selenium.webdriver.common.by import By


class Tag(object):
    """
    Oject to hold the tag data for a scraper.

    Attributes:
        tag_type: By
            The tage type, whether its a class, id, name, or x-path
        tag_value: str
            The value of the tag.
        tag: str
            The tag itself.
    """
    def __init__(self, tag_type: By, tag_value: str, tag: str = None) -> None:
        self.tag_type = tag_type
        self.tag_value = tag_value
        self.tag = tag
        super().__init__()

    @property
    def tag_type_soup(self):
        """
        Returns the tag type as a string.

        Returns:
            str: The tag type as a string.
        """
        if self.tag_type == By.CLASS_NAME:
            return 'class'
        elif self.tag_type == By.ID:
            return 'id'
        elif self.tag_type == By.NAME:
            return 'name'
        elif self.tag_type == By.XPATH:
            return 'xpath'
        else:
            return None
