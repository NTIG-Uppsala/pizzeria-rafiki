# Utgår ifrån https://github.com/jsoma/selenium-github-actions
import unittest
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.common.by import By

class CheckSiteAvailability(unittest.TestCase):
    """
        Class to handle the tests for the website
        The class also inherit python's 'unittest.TestCase' to run the test methods 
    """
    website_url = "http://localhost:8000/" # Standard URL placeholder 

    def setUp(self):
        driver_path = ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install() # Initializes the driver to memory

        # Run the browser with no GUI as it needs to be able to run as a github action
        chrome_options = Options()
        chrome_options.add_argument("--headless") 

        self.browser = webdriver.Chrome(driver_path, options=chrome_options) # Initializes the browser instance with the driver
        self.addCleanup(self.browser.quit) # Closes browser instance when tests are done

    # Test to check if "pizzeria rafiki" is in the <title> of the page
    def test_page_title(self):
        self.browser.get(self.website_url)
        self.assertIn('Pizzeria Rafiki', self.browser.title) 

    def test_check_for_company_info(self):
        information = {
            "company_name": "Pizzeria Rafiki",
            "telefon_number": "Telefonnummer: 0630-555-555",
            "adress": "Adress: Fjällgatan 32H 981 39 Flen",
            "open_hours": "Öppet:",
            "monday": "Måndagar 10-22",
            "tuesday": "Tisdagar 10-22",
            "wednesday": "Onsdagar 10-22",
            "thusday": "Torsdagar 10-22",
            "friday": "Fredagar 10-23",
            "saturday": "Lördagar 12-23",
            "sunday": "Söndagar 12-20",
            "mail_adress": "Mailadress: info@rafiki.se"
        }

        self.browser.get(self.website_url)

        body_text = self.browser.find_element(By.TAG_NAME, "body").text # Grab all text from the page body

        # Check each values from the dict if they are present on the webpage
        for info_value in information.values():
            self.assertIn(info_value, body_text)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        CheckSiteAvailability.website_url = sys.argv.pop() # Change url to passed in argument
        unittest.main(verbosity=2) # Run unit tests
    else:
        # Throw error if no arguments when running python script
        raise Exception("No url passed in as arugment")