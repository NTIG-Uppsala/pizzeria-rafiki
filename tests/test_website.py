# Utgår ifrån https://github.com/jsoma/selenium-github-actions
from datetime import datetime, timedelta
from types import NoneType
import unittest
import sys
from datetime import datetime
import time
import re
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CheckSiteAvailability(unittest.TestCase):
    """
        Class to handle the tests for the website
        The class also inherit python's 'unittest.TestCase' to run the test methods 
    """
    website_url = "http://localhost:8000/" # Standard URL placeholder 

    def setUp(self):

        # Run the browser with no GUI as it needs to be able to run as a github action
        run_options = FirefoxOptions()
        run_options.add_argument("--headless") 
        
        path_to_binaries = Path(__file__).resolve().parents[1] / Path('bin')
        if sys.platform == "win32":
            self.browser = webdriver.Firefox(service=FirefoxService(executable_path=path_to_binaries/Path('geckodriver.exe')), options=run_options) # Initializes the browser instance with the driver
        else:
            self.browser = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=run_options) # Initializes the browser instance with the driver

        self.addCleanup(self.browser.quit) # Closes browser instance when tests are done

    # Test to check if "pizzeria rafiki" is in the <title> of the page
    def test_page_title(self):
        self.browser.get(self.website_url)
        self.assertIn('Pizzeria Rafiki', self.browser.title) 

    def test_check_for_contact(self):
        information = {
            "phone_number": "0630-555-555",
            "adress": "Fjällgatan 32H 981 39 Flen",
            "mail_adress": "info@rafiki.se"
        }
        
        self.browser.get(self.website_url)
        
        self.assertIn('mailto:info@rafiki.se', self.browser.find_element(By.ID, "MailAdress").get_attribute("href"))
        self.assertIn('tel:0630-555-555', self.browser.find_element(By.ID, "PhoneNumber").get_attribute("href"))

        body_text = self.browser.find_element(By.TAG_NAME, "body").text.replace('\n', ' ') # Grab all text from the page body

        # Check each values from the dict if they are present on the webpage
        for info_value in information.values():
            self.assertIn(info_value, body_text)

    
    def test_check_for_open_hours(self):
        self.browser.get(self.website_url)

        # Dict of open hours
        open_hours = {
            "Monday": ["Måndagar","10-22"],
            "Tuesday": ["Tisdagar","10-22"],
            "Wedensday": ["Onsdagar","10-22"],
            "Thursday": ["Torsdagar", "10-22"],
            "Friday": ["Fredagar", "10-23"],
            "Saturday": ["Lördagar", "12-23"],
            "Sunday": ["Söndagar", "12-20"],
        }

        open_hours_table = self.browser.find_element(By.ID, "OpenHours")
        open_hours_elements = open_hours_table.find_elements(By.TAG_NAME, "tr")

        for open_hour in open_hours_elements:
            current_day = open_hour.get_attribute("data-day")
            listing_text = open_hour.text
            
            # If a tr has no data-day attribute skip it
            if isinstance(current_day, NoneType):
                continue
            
            if current_day in listing_text:
                self.assertIn(" ".join(open_hours[current_day]), listing_text)

    
    def check_image(self, x):
        # get the elment with the Background class name
        background_element = self.browser.find_element(By.CLASS_NAME, "Background")

        # Get the background-image value
        css_value = background_element.value_of_css_property("background-image")
        
        # return if background{number}.jpg is in the css_value
        return "background{}.jpg".format(x) in css_value


    def test_for_background(self):
        self.browser.get(self.website_url)
        
        # Initilize a WebDriverWait object passing in the browser driver and a 30 sec timeout
        wait = WebDriverWait(self.browser, 30)
        
        # lambda function to call the check_image method
        check_image_lambda = lambda _ : self.check_image(str(i))

        # Itterate through all images 1-3 to check if they are shown on the page
        for i in range(1, 4):
            wait.until(check_image_lambda, "Timeout")
            print("Wait done")   
            

    def read_svg_data(self, file_name):
        # Get the path to the file
        icon_path = Path(__file__).resolve().parents[1] / Path(f'src/assets/images/{file_name}')
        
        # Reads the svg data from the the icon_path
        with open(icon_path, 'r+') as file:
            # Converts the data to one line, replacing newlines and multiple whitespaces with no space
            file_data = ''.join(file.readlines()).replace('\n', '')
            
            return file_data

    # Three tests to check if the correct icons are used on the webpage    
    def test_check_for_socials(self):
        self.browser.get(self.website_url)

        icons = [
            ['FacebookIcon', 'facebook-circle-fill.svg'],
            ['InstagramIcon', 'instagram-fill.svg'],
            ['TwitterIcon', 'twitter-fill.svg']
        ]

        # For each icon in the icons list
        for icon in icons:
            print("current icon check:", icon[0])

            # Get the icon[0] element from page
            icon_element = self.browser.find_element(By.CLASS_NAME, icon[0])

            # Get the css property value background-image and href attribute
            icon_css_value = icon_element.value_of_css_property("background-image").replace('\\', '')
            icon_href = icon_element.get_attribute('href')

            # Assert if correct link and correct svg path
            self.assertIn('NTIuppsala', icon_href)
            self.assertIn(icon[1], icon_css_value)

    
    def test_check_for_products(self):
        self.browser.get(self.website_url)

        # List of products
        products = {
            "Capricciosa": ["skinka, champinjoner", "90 kr"], 
            "Calzone": ["inbakad, skinka", "85 kr"], 
            "Margherita": ["ost", "80 kr"],
            "Hawaii": ["skinka, ananas", "90 kr"],
            "Vesuvio": ["skinka", "85 kr"], 
            "Extra topping": ["5 kr"],
            "Pompei": ["bacon, rödlök, ägg, curry", "90 kr"],
            "La Casa": ["champinjoner, räkor, skinka", "95 kr"]
        }

        products_table = self.browser.find_element(By.ID, "Products")
        page_products_element = products_table.find_elements(By.TAG_NAME, "tr")

        # Loop through the products table element
        for product in page_products_element:
            # Get the data-pizza attribute value
            pizza = product.get_attribute("data-pizza")
            listing_text = product.text

            # If the data attribute is a None Type, skip to the next element
            if isinstance(pizza, NoneType):
                continue
            
            # Compare the Dictionary to the page value
            if pizza in listing_text:
                self.assertIn(" ".join(products[pizza]), listing_text)

    def test_check_for_logo(self):
        self.browser.get(self.website_url)

        # Gets header logo element and favicon element
        favicon_element = self.browser.find_element(By.XPATH, "//link[@type='image/x-icon']")
        header_icon_element = self.browser.find_element(By.CLASS_NAME, "Logo")

        # Checks if correct logo file is in src and href
        self.assertIn('rafikilogofavicon.png', favicon_element.get_attribute('href'))
        self.assertIn('rafikilogo.svg', header_icon_element.value_of_css_property('background-image'))

    def test_for_large_images(self):
        # Get path for image folder
        image_path = Path(__file__).resolve().parents[1] / Path('src/assets/images/')
        
        # Assert check for images larger than 1Mb
        for image in image_path.glob('**/*.*'):
            image_size = Path(image).stat().st_size
            print("Image path: {} \t image size: {}".format(image, image_size))
            self.assertGreater(5e5, image_size)

    def test_screenshot(self):
        self.browser.get(self.website_url)
    
        resolutions = [
            [2560, 1440], # 2k desktop
            [1920, 1080], # desktop
            [1440, 1080], # laptop
            [820, 1180], # iPad Air
            [390, 844], # iPhone 12 Pro
        ]

        for res in resolutions:
            x,y = res

            date = str(datetime.now())

            self.browser.set_window_position(0, 0)
            self.browser.set_window_size(x, y)
            self.browser.save_screenshot("screenshots/screenshot" + re.sub(r'[\W_]+', '', date) + str(x) + "x" + str(y) + ".png")
            
            print("saved screenshot with resolution", x, y)
    
    def test_map(self):
        self.browser.get(self.website_url)
        self.browser.find_element(By.ID, "Map")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        CheckSiteAvailability.website_url = sys.argv.pop() # Change url to passed in argument
        unittest.main(verbosity=2) # Run unit tests
    else:
        # Throw error if no arguments when running python script
        raise Exception("No url passed in as argument")