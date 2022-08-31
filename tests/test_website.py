# Utgår ifrån https://github.com/jsoma/selenium-github-actions
import unittest
import sys
import re
from pathlib import Path
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

    # Test to check for background image in css
    def test_check_for_background_image(self):
        self.browser.get(self.website_url)
        
        # Locate element with class .BackgroundImage and get its background-image css value
        css_background_value = self.browser.find_element(By.CLASS_NAME, "HeaderImage")

        # test if background.jpg is in the value of css property background-image
        self.assertIn('background.jpg', css_background_value.value_of_css_property("background-image") ) 

    def test_check_for_product_image1(self):
        self.browser.get(self.website_url)
        
        # Locate element and get its product-image value
        product_element1 = self.browser.find_element(By.XPATH, '//img[@src="assets/images/prod1.jpg"]')

        # test if prod1.jpg is on the website 
        self.assertIn('prod1.jpg', product_element1.get_attribute('src'))

    def test_check_for_product_image2(self):
        self.browser.get(self.website_url)
        
        # Locate element with class .BackgroundImage and get its background-image css value
        product_element2 = self.browser.find_element(By.XPATH, '//img[@src="assets/images/prod2.jpg"]')

        # test if background.jpg is in the value of css property background-image
        self.assertIn('prod2.jpg', product_element2.get_attribute('src'))

    def read_svg_data(self, file_name):
        # Get the path to the file
        icon_path = Path(__file__).resolve().parents[1] / Path(f'src/assets/images/{file_name}')
        
        # Reads the svg data from the the icon_path
        with open(icon_path, 'r+') as file:
            # Converts the data to one line, replacing newlines and multiple whitespaces with no space
            file_data = ''.join(file.readlines()).replace('\n', '')
            
            return file_data

    def test_check_for_facebook_icon(self):
        self.browser.get(self.website_url)
        facebook_css_element = self.browser.find_element(By.CLASS_NAME, "FacebookIcon")
        
        file_data = self.read_svg_data('facebook-circle-line.svg')

        self.assertIn(file_data, facebook_css_element.value_of_css_property("background-image").replace('\\', ''))
            
    def test_check_for_instagram_icon(self):
        self.browser.get(self.website_url)
        instagram_css_element = self.browser.find_element(By.CLASS_NAME, "InstagramIcon")
        
        file_data = self.read_svg_data('instagram-line.svg')

        self.assertIn(file_data, instagram_css_element.value_of_css_property("background-image").replace('\\', ''))
           

    def test_check_for_twitter_icon(self):
        self.browser.get(self.website_url)
        twitter_css_element = self.browser.find_element(By.CLASS_NAME, "TwitterIcon")
        
        file_data = self.read_svg_data('twitter-line.svg')

        self.assertIn(file_data, twitter_css_element.value_of_css_property("background-image").replace('\\', ''))
           
    

if __name__ == '__main__':
    if len(sys.argv) > 1:
        CheckSiteAvailability.website_url = sys.argv.pop() # Change url to passed in argument
        unittest.main(verbosity=2) # Run unit tests
    else:
        # Throw error if no arguments when running python script
        raise Exception("No url passed in as arugment")