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


class Args(object):
    """
    The arguments for a Website.

    Attributes:
        types: list[str]
            The type of the arguments to pass to the url.
        values: list[str]
            The values of the arguments to pass to the url.
    """
    def __init__(self, types: list[str], values: list[str]=[]) -> None:
        self.types = types
        self.values = values
        super().__init__()

    def value_for(self, type_: str, value=None) -> str:
        """
        Return the value for the type.

        Params:
            - type_: str
                The type of the value.
            - value: str
                The value to return if the type is not found.

        Returns:
            str: The value for the type.
        """
        # Return the value.
        if self.types.index(type_) < len(self.values):
            return self.values[self.types.index(type_)]
        else:
            return value