import json
import pathlib
import os

from selenium import webdriver



class BrowserDriver():

    def __init__(self, browser):
        self._configs = json.load(open(os.path.join(pathlib.Path().absolute(), 'config', 'browsers.json')))[browser]
        print(self._configs)
        
        
    def start(self):
    
        if (self._driver):
            self._driver.implicitly_wait(self._configs['implicit_wait'])
            #self._driver.maximize_window()
            
    def _add_options(self, options, args=[]):
        for option in args:
            options.add_argument(option)
        return options
        
        

class ChromeDriver(BrowserDriver):
    def __init__(self):
        super().__init__('chrome')
        
        
    def start(self):
        from selenium.webdriver.chrome.service import Service as ChromeService
        from webdriver_manager.chrome import ChromeDriverManager
        
        options = self._add_options(webdriver.ChromeOptions(), self._configs['options'])
        wdriver = webdriver.Chrome(service=ChromeService(executable_path=ChromeDriverManager().install()), options=options)
        self._driver = wdriver
        super().start()


class FirefoxDriver(BrowserDriver):
    def __init__(self):
        super().__init__('firefox') 
        
        
    def start(self):
        from selenium.webdriver.firefox.service import Service as FirefoxService
        from webdriver_manager.firefox import GeckoDriverManager
        
        wdriver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        self._driver = wdriver
        super().start()
    

class EdgeDriver(BrowserDriver):
    def __init__(self):
        super().__init__('edge')
        
    def start(self):
        from selenium.webdriver.edge.service import Service as EdgeService
        from webdriver_manager.microsoft import EdgeChromiumDriverManager
        
        wdriver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
        self._driver = wdriver
        super.start()


def factory(browser = 'chrome'):
        if (browser == 'chrome'):
            return ChromeDriver()
        elif (browser == 'firefox'):
            return FirefoxDriver()
        elif (browser == 'edge'):
            return EdgeDriver()
        else:
            raise ValueError(browser)
            

    
    
        