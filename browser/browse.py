# Script for interacting with web through selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class InteractiveBrowser:
    
    def __init__(self, initial_url="https://google.com/", debug=False):
        self.__setup_browser(initial_url, debug)

    def current_url(self):
        return self.browser.current_url

    def __setup_browser(self, url, debug):
        """
        Setup the browser.

        Params:
            - <url: str> The url the browser should start on
        """
        options = Options()
        if not debug:
            options.headless = True
            options.add_argument("--log-level=1")

        self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self.browser.get(url)
    
    def get_page(self):
        """
        Return the HTML page content of the current url.
        """
        return self.browser.page_source
    
    def send_search(self, tag=(), query="", results_tag=()):
        """
        Send a search request to the page.

        Params:
            - <tag: tupple(tag_type: str, tag_value: str)> the tag data for the html lookp
            - <query: str> what to send to the tag.

        Return: <webdriver.Restuls|False>
        """
        results = self.grab_data_from_tags(tag)
        # Chequea si tags son empty
        if not results:
            return False
        
        # Query search
        results[0].send_keys(query)
        results[0].submit()

        if results_tag:
            # Query results_tag this time
            results = self.grab_data_from_tags(results_tag)

        return results or False

    def grab_data_from_tags(self, tag) -> list:
        """
        Grab the dat from the tag info passed.

        Param:   
            - <tag: (tav_type: str, tav_value: str)>

        Return: List
        """
        # Grab data passed
        (tag_type, tag_value) = tag
        # If else to grab correct data
        if tag_type == "id":
            tags = self.browser.find_elements_by_id(tag_value)
        elif tag_type == "class":
            tags = self.browser.find_elements_by_class_name(tag_value)
        elif tag_type == "name":
            tags = self.browser.find_elements_by_name(tag_value)
        elif tag_type == "x-path":
            tags = self.browser.find_elements_by_xpath(tag_value)
        else:
            tags = []

        return tags

    def change_page(self, url):
        """
        Go to new url in browser.

        Params:
            - <url: str> the url in question
        """
        if url:
            self.browser.get(url)