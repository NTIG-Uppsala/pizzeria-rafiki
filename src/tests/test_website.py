# Utgår ifrån https://github.com/jsoma/selenium-github-actions
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.common.by import By


class CheckSiteAvailability(unittest.TestCase):
    """
        Om skriptet failar första test ("test_page_title")
        så betyder det att hemsidan inte är online och körs
    """
    def setUp(self):

        driver_path = ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install() # installerar drivern i minnet

        chrome_options = Options() # 
        chrome_options.add_argument("--headless") # 

        self.browser = webdriver.Chrome(driver_path, options=chrome_options) # Initilserar chrome drivern från den nerladdade
        self.addCleanup(self.browser.quit) # stäng webläsaren när testen är klar

        self.website_url = "http://127.0.0.1:8000/" # Urln som kommer användas

    # Test som kollar ifall Pizzeria rafiki finns med i titeln på sidan pizzeria-rafiki.github.io
    def test_page_title(self):
        self.browser.get(self.website_url)
        self.assertIn('Pizzeria Rafiki', self.browser.title) # Testa ifall "Pizzera Rafiki" är med i titlen på browsern

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

        for info_value in information.values():
            self.assertIn(info_value, self.browser.find_element(By.TAG_NAME, "body").text)



if __name__ == '__main__':
    unittest.main(verbosity=2)