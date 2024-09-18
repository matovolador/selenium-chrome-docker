from modules import database
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from enum import Enum
from time import sleep
from logger import Logger
from datetime import datetime


logging = Logger().get_logger()


db = next(database.get_db())


class BaseScraper:

    class SelectorType(Enum):
        CLASS_NAME = By.CLASS_NAME
        CSS_SELECTOR = By.CSS_SELECTOR
        TAG_NAME = By.TAG_NAME
        X_PATH = By.XPATH

    def __init__(self, proxy=None):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        if proxy:
            chrome_options.add_argument(f'--proxy-server={proxy}')
            logging.info(f"Using proxy: {proxy}")

        self.driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=chrome_options)
        logging.info("Base Scraper Initialized")
        self.start_time = datetime.now().astimezone()
        self.end_time = None
        self.time_elapsed = None
        logging.info(f"Start time: {self.start_time}")

    def get_current_url(self):
        return self.driver.current_url

    def wait(self, wait_condition_type: 'BaseScraper.SelectorType', wait_condition_element_name, wait_condition_delay=30, not_present=False):
        if not isinstance(wait_condition_type, BaseScraper.SelectorType):
            raise Exception(
                "Invalid wait_condition_type, must be of type SelectorType")

        wait_condition_type_obj = wait_condition_type.value

        try:
            if not not_present:
                WebDriverWait(self.driver, wait_condition_delay).until(
                    EC.visibility_of_element_located((wait_condition_type_obj, wait_condition_element_name)))
            else:
                WebDriverWait(self.driver, wait_condition_delay).until(
                    EC.invisibility_of_element_located((wait_condition_type_obj, wait_condition_element_name)))
        except Exception as e:
            raise Exception(e)

    def open_url(self, url, wait_condition_type: 'BaseScraper.SelectorType', wait_condition_element_name, wait_condition_delay=30):
        logging.info(f"Loading url {url}")
        self.driver.get(url)
        self.wait(wait_condition_type, wait_condition_element_name,
                  wait_condition_delay)
        logging.info("Page loaded.")

    def scroll_into_view(self, element):
        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);", element)

    def js_click(self, element):
        self.driver.execute_script("arguments[0].click();", element)

    def get_element(self, selector_type: 'BaseScraper.SelectorType', selector_value, as_list=False, element_container=None):
        if not isinstance(selector_type, BaseScraper.SelectorType):
            raise Exception(
                "Invalid selector_type, must be of type SelectorType")
        selector = selector_type.value
        if not as_list:
            if not element_container:
                return self.driver.find_element(selector, selector_value)
            else:
                return element_container.find_element(selector, selector_value)
        else:
            if not element_container:
                return self.driver.find_elements(selector, selector_value)
            else:
                return element_container.find_elements(selector, selector_value)

    def send_input(self, input_element, keys, clear_first=True):
        if clear_first:
            input_element.clear()
        input_element.send_keys(keys)

    def click(self, element):
        element.click()

    def execute_script(self, script, element, is_async=False):
        if is_async:
            self.driver.execute_async_script(script, element)
        else:
            self.driver.execute_script(script, element)

    def set_element_property_value(self, element, prop, value):
        self.execute_script(f"arguments[0].{prop} = '{value}';", element)

    def sleep(self, sleep_for_seconds):
        logging.info(f"Sleeping for {sleep_for_seconds} seconds")
        sleep(sleep_for_seconds)

    def quit(self):
        self.end_time = datetime.now().astimezone()
        logging.info(f"End time {self.end_time}")
        time_difference = self.end_time - self.start_time
        self.time_elapsed = time_difference.total_seconds()
        logging.info(
            f"Time elapsed: {self.time_elapsed} seconds.")
        logging.info("Destroying driver")
        try:
            self.driver.quit()
        except Exception as e:
            logging.error(f"Error quitting driver: {e}")
