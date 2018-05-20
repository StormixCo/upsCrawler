from sys import platform
import os
import time

# Import Selenium modules
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Crawler:
    
    browser = None
    delay = 3

    def __init__(self,target):
        self.target = target
        
    
    def launchBrowser(self):
        assert not self.browser, "Browser already set !"
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        # Initiate the Browser webdriver
        currentfolder = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))
        # Check which operating system is being used !
        if platform == "linux" or platform == "linux2":
            # linux
            chrome_driver = currentfolder+"/Drivers/chromedriver"
        elif platform == "win32":
            # Windows
            chrome_driver = "Drivers/chromedriver.exe"
        print("Chrome Driver Location : "+chrome_driver)
        self.browser = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
    
    def goToSite(self,url = None):
        Browser = self.browser
        Website = self.target if not url else url
        # Open Website
        Browser.get(Website)
        print("Browser Initiated !")
        print("Loading .. " + Website, end =' ')
        time.sleep(self.delay)
        print('[DONE]')
