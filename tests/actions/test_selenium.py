import unittest
import os
import pathlib
import tass.actions.selenium as selenium
from tass.drivers.browserdriver import ChromeDriver as Chrome
from tass.drivers.browserdriver import FirefoxDriver as Firefox
from tass.drivers.browserdriver import EdgeDriver as Edge
import selenium.webdriver.support.expected_conditions as EC


class TestSelenium(unittest.TestCase):

    config = {
            "implicit_wait":5,
            "explicit_wait":10,
            "options": ["--start-maximized"]
            } 
    
    test_page_url = 'tests/pages/page1.html'

    def tearDown(self):
        self.driver.quit()

    def setUp(self):
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("Beginning new test TestCase %s" % self._testMethodName)
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        
        self.driver = Chrome(self.config);
        self.driver.implicit_wait_from_config()
        
    def test_SeleniumLoadURL(self):
        url = "https://www.google.ca"
        selenium.load_url(self.driver, url)
        self.assertEqual(self.driver.title, "Google")
    
    def test_SeleniumLoadFile(self):
        selenium.load_file(self.driver, self.test_page_url)
        self.assertEqual(self.driver.title, "Page One")
        
    def test_SeleniumClick(self):
        url = os.path.join(pathlib.Path().resolve(), self.test_page_url)
        self.driver.get('file://' + url)
        selenium.click(self.driver, locator={"by": "id", "value": "btnColor"})
        self.assertIsNotNone(self.driver.wait_until(
                until_func=EC.presence_of_element_located,
                locator=("xpath", "//button[contains(@style, 'salmon')]")))
    
    def test_SeleniumType(self):
        url = os.path.join(pathlib.Path().resolve(), self.test_page_url)
        self.driver.get('file://' + url)
        text = 'Selenium Test Type'
        selenium.type(self.driver, text=text, locator={"by": "id", "value": "nameField"})
        self.assertEqual(self.driver.find_element('id', 'nameField').get_attribute('value'), text)
        
    def test_SeleniumReadAttribute(self):
        url = os.path.join(pathlib.Path().resolve(), self.test_page_url)
        self.driver.get('file://' + url)
        self.assertEqual(selenium.read_attribute(
                self.driver, attribute='name',
                locator={"by": "id", "value": "btn2"}), 'button2')
                
    def test_SeleniumReadCSS(self):
        url = os.path.join(pathlib.Path().resolve(), self.test_page_url)
        self.driver.get('file://' + url)
        self.assertEqual(selenium.read_css(
                self.driver, attribute='width',
                locator={"by": "id", "value": "btn1"}), '300px')
