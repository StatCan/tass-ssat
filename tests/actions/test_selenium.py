import unittest
import tass.actions.selenium as selenium
from tass.drivers.browserdriver import ChromeDriver as Chrome
from tass.drivers.browserdriver import FirefoxDriver as Firefox
from tass.drivers.browserdriver import EdgeDriver as Edge

#TODO: Add a description of what the class does

class TestSelenium(unittest.TestCase):
    
    config = {
            "implicit_wait":5,
            "explicit_wait":10,
            "options": ["--start-maximized"]
            }
            
    #driver = Chrome(config)
    
    @classmethod
    def setUpClass(cls):
        cls.driver = Chrome(cls.config);
        
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("Beginning new test TestCase %s" % self._testMethodName)
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        
    
    def test_SeleniumLoadFile(self):
        url = 'tests/pages/page1.html'
        selenium.load_file(self.driver, url)
        import time
        time.sleep(10)
            
