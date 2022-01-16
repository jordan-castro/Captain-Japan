# This handles the basic functions of a CaptainJapan scraper.

from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import requests
import time

from cj.utils.exceptions import NoJsException, NoScrollException


class Scraper:
    """
    Implements the abstract Base class and handles some basic scraping neccesities.

    Methods:
        - soupify(self): Returns a BeatifulSoup object, based on the current page.
        - try_click(self): Attempt to click on a element on the browser.
        - wait(self, t): Wait for [t] seconds.
        - get_url(self, url): Move the browser to a new url.

    Params:
        - headless(bool): Is the browser headless?
        - javascript(bool): Is the website being loaded with JavaScript?
        - start_url(str): The url to start on, defaults to https://www.google.com.
    """
    # The limit of scrapes to be done at a time. (if js is enabled then it will be the amount of pages before waiting)
    limit: int = 5

    def __init__(self, javascript:bool, headless:bool, start_url:str="https://www.google.com") -> None:
        self.js = javascript
        self.current_url = start_url
        self.driver = None
        self.scroll_distance = 250
        self.should_scroll = False
        self.should_wait = True
        self.wait_time = 0.5

        self.previous_scroll_distance = self.scroll_distance
        self.previous_wait_time = self.wait_time
        self.previous_should_scroll = self.should_scroll
        self.previous_should_wait = self.should_wait

        self.can_change_scroll = True
        self.can_change_wait = True

        # If JS is enabled, setup the browser.
        if self.js:
            self._setup_js(headless)

    def _setup_js(self, headless):
        """
        Setup a browser for those websites that load with JavaScript.

        Params:
            - headless(bool): Is this a headless browser?
        """
        options = Options()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")

        # Add some headers to make the website think we're a real browser.
        options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36")
        options.add_argument("accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9")
        options.add_argument("accept-language=en-US,en;q=0.9")
        
        # Create the browser.
        self.driver = uc.Chrome(options=options)
        self.driver.set_window_position(0, 0)
        self.driver.set_window_size(1920, 900)

        # Load to the start url, which is currently self.current_url.
        self.driver.get(self.current_url)

    def soup(self):
        """
        Returns a BeatifulSoup object, based on the current page.
        """
        try:
            # Get the url source
            source = self.get_url(self.current_url, True)
            # Check if None
            if source is None:
                return None
            
            # Return the soup
            return BeautifulSoup(source, "html.parser")
        # Catch any exceptions 
        except Exception as e:
            message = f"[ERROR] could not get url source of {self.current_url} because of: {e}"
            print(message)
            return None

    def get_url(self, url, r=False):
        """
        Get a url's page html content.

        Params:
            - url(str): The url to get.
            - r(bool): Return the page contents?
            - t(int): The time to wait for page content to load.

        Returns:
            - if r the page contents else None
        """
        # Check if js is enabled. If so then use the driver, otherwise use requests.
        try:
            if self.js:
                self.driver.get(url)
                self.wait()
                # Check if we should scroll the page
                if self.should_scroll:
                    # Scroll the page
                    self.scroll_page()
                response = self.driver.page_source
            else:
                response = requests.get(url).text
            self.current_url = url
        except:
            return None

        # Return the response if r is true.
        if r:
            return response

    def scroll_page(self):
        """
        Scroll the page to the bottom.
        """
        if not self.should_scroll:
            raise NoScrollException
        if not self.js:
            raise NoJsException

        # Scroll the page to the bottom.
        height = self.driver.execute_script("return document.body.scrollHeight")
        # We want to scroll the page by 250 pixels at a time until it's at the bottom.
        while 1:
            current_height = self.driver.execute_script("return window.pageYOffset")
            # Check that the new height is at least big enough
            if current_height > height - self.scroll_distance:
                break

            # Scroll the page
            self.driver.execute_script(f"window.scrollTo(0, {current_height + self.scroll_distance});")
            time.sleep(0.5)
        
        self.reset_scroll()

    def try_click(self, element, index:int=0):
        """
        Attempt to click on a element with Selenium.

        Params:
            - element(Element||list(Element)): The element(s) to try and click on.
            - index(int): The index of the element to click on.
        """
        # Check if is js
        if not self.js:
            # Raise a the no js exception
            raise NoJsException

        # If the element is a list, then click on the index.
        if isinstance(element, list):
            if index < 0 or index >= len(element):
                raise IndexError("Index out of range")
            element[index].click()
        # If the element is not a list, then click on it.
        else:
            element.click()

    def set_wait_time(self, wait):
        if self.can_change_wait:
            self.previous_wait_time = self.wait_time
            self.wait_time = wait

    def set_scroll_distance(self, distance):
        if self.can_change_scroll:
            self.previous_scroll_distance = self.scroll_distance
            self.scroll_distance = distance

    def set_should_wait(self, should):
        if self.can_change_wait:
            self.previous_should_wait = self.should_wait
            self.should_wait = should

    def set_should_scroll(self, should):
        if self.can_change_scroll:
            self.previous_should_scroll = self.should_scroll
            self.should_scroll = should

    def wait(self):
        """
        Wait a certain amount of time.
        """
        if self.should_wait:
            time.sleep(self.wait_time)
            self.reset_wait()

    def reset_wait(self):
        self.should_wait = self.previous_should_wait
        self.wait_time = self.previous_wait_time

    def reset_scroll(self):
        self.should_scroll = self.previous_should_scroll
        self.scroll_distance = self.previous_scroll_distance

    def reset_all(self):
        self.reset_wait()
        self.reset_scroll()

    def quit(self):
        """
        quit the browser.
        """
        self.driver.quit()