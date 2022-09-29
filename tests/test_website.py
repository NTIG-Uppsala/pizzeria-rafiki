# Utgår ifrån https://github.com/jsoma/selenium-github-actions
from datetime import datetime
from traceback import print_tb
from types import NoneType
import unittest
import sys
from datetime import datetime
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
            # Initializes the browser instance with the driver
            self.browser = webdriver.Firefox(service=FirefoxService(executable_path=path_to_binaries/Path('geckodriver.exe')), options=run_options)
        else:
            # Initializes the browser instance with the driver
            self.browser = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=run_options)

        self.addCleanup(self.browser.quit) # Closes browser instance when tests are done

    # Test to check if "pizzeria rafiki" is in the <title> of the page
    def test_page_title(self):
        self.browser.get(self.website_url)
        self.assertIn('Pizzeria Rafiki', self.browser.title)

    # checks for empty links
    def test_check_for_empty_links(self):
        self.browser.get(self.website_url)

        links = self.browser.find_elements(By.TAG_NAME, "a")

        for link in links:
            self.assertNotEqual(link.get_attribute("href").split("/")[-1], "#")
            self.assertIsNotNone(link.get_attribute("href"))

    # checks switch between websites
    def test_swedish_to_persian(self):
        self.browser.get(self.website_url)
        self.assertIn((self.website_url + "index-per.html"), self.browser.find_element(By.ID, "flag").get_attribute("href"))

    # Test for contact information
    def test_check_for_contact(self):
        information = {
            "phone_number": "0630-555-555",
            "adress": "Kungsvägen 2B 642 34 Flen",
            "mail_adress": "info@rafiki.se"
        }
        self.browser.get(self.website_url)
        
        self.assertIn('mailto:info@rafiki.se', self.browser.find_element(By.ID, "MailAdress").get_attribute("href"))
        self.assertIn('tel:0630-555-555', self.browser.find_element(By.CLASS_NAME, "PhoneNumber").get_attribute("href"))

        # Grab all text from the page body
        body_text = self.browser.find_element(By.TAG_NAME, "body").text.replace('\n', ' ') 

        # Check each values from the dict if they are present on the webpage
        for info_value in information.values():
            self.assertIn(info_value, body_text)

    # checks for important information on the website
    def test_check_info_on_page(self):
        self.browser.get(self.website_url)

        openHourText = self.browser.find_element(By.CLASS_NAME, "Openhours").text.replace("\n", " ")
        productText = self.browser.find_element(By.CLASS_NAME, "products").text.replace("\n", " ")

      
        products = [
           "Pizza", "Pris",
           "Margherita", "Ost", "80 kr",
           "Calzone", "Inbakad: skinka", "85 kr",
           "Vesuvio", "Skinka", "85 kr",
           "Capricciosa", "Skinka, champinjoner", "90 kr",
           "Hawaii", "Skinka, ananas", "90 kr",
           "Pompei", "Bacon, rödlök, ägg, curry", "90 kr",
           "La Casa", "Skinka, champinjoner, räkor", "95 kr",
           "Extra topping", "5 kr"
        ]


        openHours = [
            "Måndagar", "10 - 22",
            "Tisdagar", "10 - 22",
            "Onsdagar", "10 - 22",
            "Torsdagar", "10 - 22",
            "Fredagar", "10 - 23",
            "Lördagar", "12 - 23",
            "Söndagar", "12 - 20"
        ]

        for hours in openHours:
            self.assertIn(hours, openHourText)
        print("Open hours found")

        for product in products:
            self.assertIn(product, productText)
        print("Products found")


    def check_image(self, x):

        # get the elment with the Background class name
        background_element = self.browser.find_element(By.CLASS_NAME, "Background")

        # Get the background-image value
        css_value = background_element.value_of_css_property("background-image")
        
        # return if background{number}.jpg is in the css_value
        return "background{}.jpg".format(x) in css_value


    def test_for_background(self):
        self.browser.get(self.website_url)

        # Itterate through all images 1-3 to check if they are shown on the page
        for i in range(1, 4):
            self.check_image(str(i))      

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

        # Assert check for images larger than 500kB
        for image in image_path.glob('**/*.*'):
            image_size = Path(image).stat().st_size
            print("Image path: {} \t image size: {}".format(image, image_size))
            self.assertGreater(500000, image_size)

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
            self.browser.save_screenshot("screenshots/screenshot" + re.sub(r'[\W_]+', '', date) + '_' + str(x) + "x" + str(y) + ".png")
            print("saved screenshot with resolution", x, y)

    def test_map_interactive(self):
        self.browser.get(self.website_url)
        self.browser.find_element(By.ID, "MapInteractive")

    def test_zipcodes(self):
        self.browser.get(self.website_url)
        zipcode = self.browser.find_element(By.ID, "number")
        submitForm = self.browser.find_element(By.ID, "submit")

        zipcodes = {
            '-12345': 'Inte ett postnummer.',
            'a12345': 'Inte ett postnummer.',
            '1': 'Inte ett postnummer.',
            '642 30': 'Vi kör ut, ring telefonnumret ovan!',
            '64230': 'Vi kör ut, ring telefonnumret ovan!',
            '642 38': 'Vi kör tyvärr inte ut till dig.',
            '64238': 'Vi kör tyvärr inte ut till dig.',
            '64239': 'Vi kör ut, ring telefonnumret ovan!',
            '642301': 'Inte ett postnummer.'
        }

        for code in zipcodes:
            zipcode.clear()
            zipcode.send_keys(code)
            submitForm.click()
            self.assertIn(zipcodes[code], self.browser.find_element(By.ID, "jsCheck").text)
    
    def test_open_sign(self):
        self.browser.get(self.website_url)
        self.assertIn('öpp', self.browser.find_element(By.ID, "OpenSign").text)

    # persian website tests

    # checks switch between websites
    def test_persian_to_swedish(self):
        self.browser.get(self.website_url + "index-per.html")
        self.assertIn((self.website_url + "index.html"), self.browser.find_element(By.ID, "flag").get_attribute("href"))

    # checks for important information on the website
    def test_check_info_on_page_persian(self):
        self.browser.get(self.website_url + "index-per.html")

        openHourText = self.browser.find_element(By.CLASS_NAME, "Openhours").text.replace("\n", " ")
        productText = self.browser.find_element(By.CLASS_NAME, "products").text.replace("\n", " ")

      
        products = [
           "پیتزا", "قیمت",
           "Margherita", "پنیر", "80 kr",
           "Calzone", "پیتزای بسته: ژامبون", "85 kr",
           "Vesuvio", "ژامبون", "85 kr",
           "Capricciosa", "ژامبون, قارچ", "90 kr",
           "Hawaii", "ژامبون, آناناس", "90 kr",
           "Pompei", "بیکن، پیاز قرمز، تخم مرغ، کاری", "90 kr",
           "La Casa", "ژامبون، قارچ، میگو", "95 kr",
           "تاپینگ های اضافی", "5 kr"
        ]


        openHours = [
            "دوشنبه", "10 - 22",
            "سه شنبه", "10 - 22",
            "چهارشنبه", "10 - 22",
            "پنجشنبه", "10 - 22",
            "جمعه", "10 - 23",
            "شنبه", "12 - 23",
            "یکشنبه", "12 - 20"
        ]

        for hours in openHours:
            self.assertIn(hours, openHourText)
        print("Open hours found")

        for product in products:
            self.assertIn(product, productText)
        print("Products found")


    def test_zipcodes_persian(self):
        self.browser.get(self.website_url + "index-per.html")
        zipcode = self.browser.find_element(By.ID, "number")
        submitForm = self.browser.find_element(By.ID, "submit")

        zipcodes = {
            '-12345': 'کد پستی نیست',
            'a12345': 'کد پستی نیست',
            '1': 'کد پستی نیست',
            '642 30': 'ما به سمت شما رانندگی می کنیم، با شماره تلفن بالا تماس بگیرید',
            '64230': 'ما به سمت شما رانندگی می کنیم، با شماره تلفن بالا تماس بگیرید',
            '642 38': 'متأسفانه ما به شما رانندگی نمی کنیم.',
            '64238': 'متأسفانه ما به شما رانندگی نمی کنیم.',
            '64239': 'ما به سمت شما رانندگی می کنیم، با شماره تلفن بالا تماس بگیرید',
            '642301': 'کد پستی نیست'
        }

        for code in zipcodes:
            zipcode.clear()
            zipcode.send_keys(code)
            submitForm.click()
            self.assertIn(zipcodes[code], self.browser.find_element(By.ID, "jsCheck").text)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        CheckSiteAvailability.website_url = sys.argv.pop() # Change url to passed in argument
        unittest.main(verbosity=2) # Run unit tests
    else:
        # Throw error if no arguments when running python script
        raise Exception("No url passed in as argument")