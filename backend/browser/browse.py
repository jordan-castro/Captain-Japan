# Script for interacting with web through selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import cloudscraper


class InteractiveBrowser:
    
    def __init__(self, initial_url="https://google.com/", debug=False, browser=None):
        self.browser = browser
        if not self.browser:
            self.__setup_browser(initial_url, debug)
        self.cloud_scrape = cloudscraper.create_scraper()

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

        # Options to bypass cloudflare detection
        options.add_argument("--log-level=1")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        # Bypass cloudflare detection
        self.browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.browser.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})

        # Clear all cookies and cache
        self.browser.delete_all_cookies()
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
        data = self.grab_data_from_tags(tag)
        # Chequea si tags son empty
        if not data:
            return False
        
        # Query search
        data[0].send_keys(query)
        data[0].submit()

        if results_tag:
            # Query results_tag this time
            results = self.grab_data_from_tags(results_tag)
            return results or False

        return True

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
            tags = self.browser.find_elements(By.ID, tag_value)
        elif tag_type == "class":
            tags = self.browser.find_elements(By.CLASS_NAME, tag_value)
        elif tag_type == "name":
            tags = self.browser.find_elements(By.TAG_NAME, tag_value)
        elif tag_type == "x-path":
            tags = self.browser.find_elements(By.XPATH, tag_value)
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

    def close_con(self):
        """
        Close the connection on the interactive browser.
        """
        self.browser.close()
        self.cloud_scrape.close()