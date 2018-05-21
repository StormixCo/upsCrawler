from sys import platform
import os
import time
import datetime
import inspect

# Import Selenium modules
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Crawler:
    
    browser = None
    delay = 2
    DownloadPath = ""
    def __init__(self,target):
        self.target = target        
    
    def launchBrowser(self,headless = False):
        assert not self.browser, "Browser already set !"
        # Initiate the Browser webdriver
        currentfolder = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))
        # Check which operating system is being used !
        if platform == "linux" or platform == "linux2":
            # linux
            chrome_driver = currentfolder+"/Drivers/chromedriver"
            DownloadPath=  currentfolder+"/Downloads"
        elif platform == "win32":
            # Windows
            chrome_driver = "Drivers/chromedriver.exe"
            DownloadPath=  currentfolder+"\Downloads"
        self.DownloadPath = DownloadPath
        print("Chrome Driver Location : "+chrome_driver)
        if headless:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            prefs = {'profile.default_content_setting_values.automatic_downloads': 1,"download.default_directory" : DownloadPath}
            chrome_options.add_experimental_option("prefs", prefs)
            self.browser = webdriver.Chrome(chrome_options=chrome_options,executable_path=chrome_driver)

        else:
            self.browser = webdriver.Chrome(executable_path=chrome_driver)

    def goToSite(self,url = None):
        Browser = self.browser
        Website = self.target if not url else url
        # Open Website
        Browser.get(Website)
        print("Browser Initiated !")
        print("Loading .. " + Website, end =' ')
        time.sleep(self.delay)
        print('[DONE]')
    
    def debugScreenShot(self):
        date = datetime.datetime.today().strftime('%Y-%m-%d')
        Browser = self.browser
        ScreenshotPath = "Debug/"+str(date)+".png"
        Browser.get_screenshot_as_file(ScreenshotPath)
        print("Screenshot taken and save to : {}".format(ScreenshotPath))

    def wait(self):
        time.sleep(self.delay)