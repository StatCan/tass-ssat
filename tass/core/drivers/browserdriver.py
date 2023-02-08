import json
import pathlib
import os

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager    
        
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
   
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager   



class WebDriverWaitWrapper():
    
    def wait_for_element(self, until_func, **kwargs):
        wait = WebDriverWait(self, 30) #TODO: pull time from config file
        return wait.until(until_func(**kwargs))


class ChromeDriver(webdriver.Chrome, WebDriverWaitWrapper):
    def __init__(self):
        options = webdriver.ChromeOptions()
        #TODO: generate Options from config file 
        options.add_argument('--start-maximized')
        super().__init__(self, service=ChromeService(executable_path=ChromeDriverManager().install()), options=options)


class FirefoxDriver(webdriver.Firefox, WebDriverWaitWrapper):
    def __init__(self):
        options = webdriver.FirefoxOptions()
        #TODO: generate Options from config file
        options.add_argument('--start-maximized')
        super().__init__(service=FirefoxService(GeckoDriverManager().install()), options=options) 
        
    

class EdgeDriver(webdriver.Edge, WebDriverWaitWrapper):
    def __init__(self):
        options = webdriver.EdgeOptions()
        #TODO: generate Options from config file
        options.add_argument('--start-maximized')
        super().__init__(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)
            

    
    
        