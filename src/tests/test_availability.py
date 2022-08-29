# Utgår ifrån https://github.com/jsoma/selenium-github-actions
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType


class CheckSiteAvailability(unittest.TestCase):
    def setUp(self):
        driver_path = ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install() # installerar drivern i minnet

        chrome_options = Options() # 
        chrome_options.add_argument("--headless") # 

        self.browser = webdriver.Chrome(driver_path, options=chrome_options) # Initiliserar chrome drivern från den nerladdade
        self.addCleanup(self.browser.quit) # stäng webläsaren när testen är klar

        self.website_url = "https://ntig-uppsala.github.io/pizzeria-rafiki/src/" # Urln som kommer användas

    # Test som kollar ifall Pizzeria rafiki finns med i titeln på sidan pizzeria-rafiki.github.io
    def test_page_title(self):
        self.browser.get(self.website_url)
        self.assertIn('Pizzeria Rafiki', self.browser.title) # Testa ifall "Pizzera Rafiki" är med i titlen på browsern

if __name__ == '__main__':
    unittest.main(verbosity=2)