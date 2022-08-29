import unittest
from selenium import webdriver

class GoogleTestCase(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome('chromedriver.exe') # Initiliserar chrome drivern
        self.addCleanup(self.browser.quit) # stäng webläsaren när testen är klar

    # Test som kollar ifall Pizzeria rafiki finns med i titeln på sidan pizzeria-rafiki.github.io
    def test_page_title(self):
        self.browser.get('pizzeria-rafiki.github.io')
        self.assertIn('Pizzeria Rafiki', self.browser.title)

if __name__ == '__main__':
    unittest.main(verbosity=2)