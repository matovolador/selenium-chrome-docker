from modules import database
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


from logger import Logger


logging = Logger().get_logger()

# now = datetime.now().astimezone()
# date_from = datetime(now.year,now.month,now.day,9,0,0,0)
# date_to = datetime(now.year,now.month,now.day,22,0,0,0)
# if (now<date_from or now>=date_to):
#     logging.info("Not running during {}".format(now))
#     exit()

db = next(database.get_db())


class BaseScraper:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=chrome_options)
        logging.info("Base Scraper Initialized")

    def wait(self, wait_condition_type, wait_condition_element_name, wait_condition_delay=30, not_present=False):
        if wait_condition_type == "class_name":
            wait_condition_type_obj = By.CLASS_NAME
        elif wait_condition_type == "css_selector":
            wait_condition_type_obj = By.CSS_SELECTOR
        elif wait_condition_type == "tag_name":
            wait_condition_type_obj = By.TAG_NAME
        elif wait_condition_type == "x_path":
            wait_condition_type_obj = By.XPATH
        else:
            raise Exception("Unhandled wait_condition_type")
        try:
            if not not_present:
                WebDriverWait(self.driver, wait_condition_delay).until(
                    EC.visibility_of_element_located((wait_condition_type_obj, wait_condition_element_name)))
            else:
                WebDriverWait(self.driver, wait_condition_delay).until(
                    EC.invisibility_of_element_located((wait_condition_type_obj, wait_condition_element_name)))
        except Exception as e:
            raise Exception(e)

    def open_url(self, url, wait_condition_type, wait_condition_element_name, wait_condition_delay=30):
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

    def get_element(self, selector_type, selector_value, as_list=False, element_container=None):
        if selector_type == "class_name":
            selector = By.CLASS_NAME
        elif selector_type == "css_selector":
            selector = By.CSS_SELECTOR
        elif selector_type == "tag_name":
            selector = By.TAG_NAME
        elif selector_type == "x_path":
            selector = By.XPATH
        else:
            raise Exception(f"Unhandled selector_type {selector_type}")

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

    def quit(self):
        logging.info("Destroying driver")
        try:
            self.driver.quit()
        except Exception as e:
            logging.error(f"Error quitting driver: {e}")
