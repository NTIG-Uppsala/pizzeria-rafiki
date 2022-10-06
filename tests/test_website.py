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


class GlobalTest(unittest.TestCase):
    """
        Class to handle the tests for the website
        The class also inherit python's 'unittest.TestCase' to run the test methods 
    """
    website_url = "" # Standard URL placeholder 

    @classmethod
    def setUpClass(self):

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

        self.pages = [
            'index.html',
            'lulea.html',
            'flen.html'
        ]

    @classmethod
    def tearDownClass(self):
        self.browser.quit()
    
    def test_check_for_empty_links(self):

        for page in self.pages:
            self.browser.get(self.website_url + page)
            print("Testing on page: {}".format(page))

            links = self.browser.find_elements(By.TAG_NAME, "a")

            for link in links:
                self.assertNotEqual(link.get_attribute(
                    "href").split("/")[-1], "#")

    def test_for_large_images(self):

        # Get path for image folder
        image_path = Path(__file__).resolve().parents[1] / Path('src/assets/images/')

        # Assert check for images larger than 500kB
        for image in image_path.glob('**/*.*'):
            image_size = Path(image).stat().st_size
            print("Image path: {} \t image size: {}".format(image, image_size))
            self.assertGreater(500000, image_size)

    def test_check_for_socials(self):
        for page in self.pages:

            self.browser.get(self.website_url + page)
            print("Testing on page: {}".format(page))
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
    
    def test_screenshot(self):
        for page in self.pages:

            self.browser.get(self.website_url + page)
            print("Testing on page: {}".format(page))

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
                self.browser.save_screenshot("screenshots/screenshot"+ page + re.sub(r'[\W_]+', '', date) + '_' + str(x) + "x" + str(y) + ".png")
                print("saved screenshot with resolution", x, y)

class PageTests(unittest.TestCase):
    """
        Class to handle the tests for the website
        The class also inherit python's 'unittest.TestCase' to run the test methods 
    """
    website_url = "" # Standard URL placeholder 


    @classmethod
    def setUpClass(self):

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

    @classmethod
    def tearDownClass(self):
        self.browser.quit()

    #INDEX TESTS

    def test_check_side_links_to_flen_and_lulea(self):
        self.browser.get(self.website_url)

        control_links = [
            "flen.html",
            "lulea.html"
        ]
        link_element = self.browser.find_element(By.CLASS_NAME, "cards")
        links = link_element.find_elements(By.TAG_NAME, "a")
        for control_link in control_links:
            self.assertIn(control_link, ([link.get_attribute("href").split('/')[-1] for link in links]))

    #FLEN TESTS

    def test_swedish_to_persian_flen(self):
        self.browser.get(self.website_url + "flen.html")
        self.assertIn((self.website_url + "flen-per.html"), self.browser.find_element(By.ID, "flag").get_attribute("href"))


    def test_check_info_on_page_flen(self):
        self.browser.get(self.website_url + "flen.html")

        openHourText = self.browser.find_element(By.CLASS_NAME, "Openhours").text.replace("\n", " ")
        productText = self.browser.find_element(By.CLASS_NAME, "products").text.replace("\n", " ")
        closedDayText = self.browser.find_element(By.CLASS_NAME, "holidays").text.replace("\n", " ")

      
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

        closedDays = [
            "Trettondedag jul", "6 Januari",
            "Första maj", "1 Maj",
            "Julafton", "24 December",
            "Juldagen", "25 December",
            "Annandag jul", "26 December"
        ]

        for hours in openHours:
            self.assertIn(hours, openHourText)
        print("Open hours found")

        for product in products:
            self.assertIn(product, productText)
        print("Products found")

        for closedDay in closedDays:
            self.assertIn(closedDay, closedDayText)
        print("Closed days found")
    
    def test_check_for_contact_flen(self):
        information = {
            "phone_number": "0630-555-555",
            "adress": "Kungsvägen 2B 642 34 Flen",
            "mail_adress": "info@rafiki.se"
        }
        self.browser.get(self.website_url + "flen.html")
        
        self.assertIn('mailto:info@rafiki.se', self.browser.find_element(By.ID, "MailAdress").get_attribute("href"))
        self.assertIn('tel:0630-555-555', self.browser.find_element(By.CLASS_NAME, "PhoneNumber").get_attribute("href"))

        # Grab all text from the page body
        body_text = self.browser.find_element(By.TAG_NAME, "body").text.replace('\n', ' ') 

        # Check each values from the dict if they are present on the webpage
        for info_value in information.values():
            self.assertIn(info_value, body_text)
    
    def test_zipcodes_flen(self):
        self.browser.get(self.website_url + "flen.html")
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

    def test_map_interactive_flen(self):
        self.browser.get(self.website_url + "flen.html")
        self.browser.find_element(By.ID, "MapInteractive")

    #LULEÅ TESTS

    def test_swedish_to_persian_lulea(self):
        self.browser.get(self.website_url + "lulea.html")
        self.assertIn((self.website_url + "lulea-per.html"), self.browser.find_element(By.ID, "flag").get_attribute("href"))


    def test_check_info_on_page_lulea(self):
        self.browser.get(self.website_url + "lulea.html")

        openHourText = self.browser.find_element(By.CLASS_NAME, "Openhours").text.replace("\n", " ")
        productText = self.browser.find_element(By.CLASS_NAME, "products").text.replace("\n", " ")
        closedDayText = self.browser.find_element(By.CLASS_NAME, "holidays").text.replace("\n", " ")

      
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
            "Onsdagar", "10 - 24",
            "Torsdagar", "10 - 22",
            "Fredagar", "10 - 03",
            "Lördagar", "12 - 04",
            "Söndagar", "12 - 23"
        ]

        closedDays = [
            "Trettondedag jul", "6 Januari",
            "Första maj", "1 Maj",
            "Julafton", "24 December",
            "Juldagen", "25 December",
            "Annandag jul", "26 December"
        ]

        for hours in openHours:
            self.assertIn(hours, openHourText)
        print("Open hours found")

        for product in products:
            self.assertIn(product, productText)
        print("Products found")

        for closedDay in closedDays:
            self.assertIn(closedDay, closedDayText)
        print("Closed days found")
    
    def test_check_for_contact_lulea(self):
        information = {
            "phone_number": "0640-555-333",
            "adress": "Färjledsvägen 38 961 93 Södra Sunderbyn Luleå",
            "mail_adress": "lulea@rafiki.se"
        }
        self.browser.get(self.website_url + "lulea.html")
        
        self.assertIn('mailto:lulea@rafiki.se', self.browser.find_element(By.ID, "MailAdress").get_attribute("href"))
        self.assertIn('tel:0640-555-333', self.browser.find_element(By.CLASS_NAME, "PhoneNumber").get_attribute("href"))

        # Grab all text from the page body
        body_text = self.browser.find_element(By.TAG_NAME, "body").text.replace('\n', ' ') 

        # Check each values from the dict if they are present on the webpage
        for info_value in information.values():
            self.assertIn(info_value, body_text)
    
    def test_zipcodes_lulea(self):
        self.browser.get(self.website_url + "lulea.html")
        zipcode = self.browser.find_element(By.ID, "number")
        submitForm = self.browser.find_element(By.ID, "submit")

        zipcodes = {
            '-12345': 'Inte ett postnummer.',
            'a12345': 'Inte ett postnummer.',
            '1': 'Inte ett postnummer.',
            '961 90': 'Vi kör ut, ring telefonnumret ovan!',
            '96190': 'Vi kör ut, ring telefonnumret ovan!',
            '961 98': 'Vi kör tyvärr inte ut till dig.',
            '96198': 'Vi kör tyvärr inte ut till dig.',
            '96193': 'Vi kör ut, ring telefonnumret ovan!',
            '961901': 'Inte ett postnummer.'
        }

        for code in zipcodes:
            zipcode.clear()
            zipcode.send_keys(code)
            submitForm.click()
            self.assertIn(zipcodes[code], self.browser.find_element(By.ID, "jsCheck").text)

    def test_map_interactive_lulea(self):
        self.browser.get(self.website_url + "lulea.html")
        self.browser.find_element(By.ID, "MapInteractive")

    


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg = sys.argv.pop()
        # Change url to passed in argument
        GlobalTest.website_url = arg
        PageTests.website_url = arg

    else:
        # if no argument is passed in, test on live website
        GlobalTest.website_url = "https://ntig-uppsala.github.io/pizzeria-rafiki/"
        PageTests.website_url = "https://ntig-uppsala.github.io/pizzeria-rafiki/"

    unittest.main(verbosity=2)  # Run unit tests