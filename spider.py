from crawler import Crawler

# Import Selenium modules
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class MathUPSpider():
    
    concours = []
    filieres = []
    matieres = []
    selects = {
        "c":"concours",
        "m":"matiere",
        "f":"filiere"
    }
    timeout = 60

    def __init__(self):
        self.target = "http://concours-maths-cpge.fr"
        self.Spider = Crawler(self.target)
    
    def __repr__(self):
        return """
        Scrapping: {}
        Currently hold : {} Concours
                         {} Filiers
                         {} matieres

        """.format(self.target,len(self.concours),len(self.filieres),len(self.matieres))

    def submit(self):
        self.clickButton("commande")

    def clickButton(self,button):
        Spider = self.Spider
        selectButton = Spider.browser.find_element_by_name(button)
        selectButton.click()
    
    def getSelectValues(self,name):
        Spider = self.Spider
        select = Select(Spider.browser.find_element_by_name(name))
        values = [(option.text,option.get_attribute("value")) for option in select.options if "tous" not in option.text and "indiff" not in option.text]
        return values

    def selectOption(self,name,value):
        Spider = self.Spider
        print("On the {} select, we'll select: {}".format(name,value))
        select = Select(Spider.browser.find_element_by_name(name))
        select.select_by_value(value)

    def fillInput(self,name,data):
        """ fills an input with the given data """
        Spider = self.Spider
        inputYear = Spider.browser.find_element_by_name(name)
        inputYear.clear()
        inputYear.send_keys(data)

    def fillinYear(self,annee):
        self.fillInput("annee",annee)

    def checkNoSubject(self):
        try:
            hidden = self.Spider.browser.find_element_by_css_selector("body > div:nth-child(2) > form > table > tbody > tr:nth-child(1) > td")
            #find_element_by_name("ordre")
            value = hidden.get_attribute("innerHTML")
            return value == "aucun sujet n'est disponible"
        except NoSuchElementException:
            return False
    
    def initVisit(self):
        """ Opens up the search form """
        Spider = self.Spider
        Spider.launchBrowser(True)
        Spider.goToSite()
        self.submit() # Clicks "connexion button"
        Spider.wait()

    def setData(self):
        """ Fetches concours,filiers,matieres from the search form"""
        self.initVisit()
        self.concours = self.getSelectValues(self.selects["c"])
        self.filieres = self.getSelectValues(self.selects["f"])
        self.matieres = self.getSelectValues(self.selects["m"])

    def openFilesTab(self,button):
        # Open files
        try:
            button.click()
        except StaleElementReferenceException:
            self.Spider.wait()
            button.click()

    def getFiles(self):
        Spider = self.Spider
        rows = Spider.browser.find_elements_by_css_selector("body > div:nth-child(2) > form > table > tbody > tr")
        rows = rows[1:-1]
        for i in range(2,len(rows)+3,2):
            currentRow = i
            selector = "body > div:nth-child(2) > form > table > tbody > tr:nth-child("+str(currentRow)+") > td > button"
            print(selector,end="\n\n")
            cols = Spider.browser.find_elements_by_css_selector("body > div:nth-child(2) > form > table > tbody > tr:nth-child("+str(currentRow)+") > td")
            colText = lambda col,i : col.text if i != 1 else col.find_element_by_css_selector("a").get_attribute("title")
            fileName = "-".join([colText(cols[i],i) for i in range(len(cols[:-1]))])
            print(fileName)
            button = WebDriverWait(Spider.browser, self.timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            try:
                self.openFilesTab(button)
            except selenium.common.exceptions.TimeoutException:
                print("Skipping this one ...")
                continue
            # Get the files
            FileTable = Spider.browser.find_element_by_css_selector("body > div:nth-child(2) > form > table > tbody > tr > td:nth-child(1) > table")
            for row in FileTable.find_elements_by_css_selector("tr"):
                cols = row.find_elements_by_css_selector("td")
                downloadButton = row.find_elements_by_css_selector("button")[-1]
                downloadButton.click()
                fileNameDownload = fileName + "-" + cols[0].text 
                print("Downloading ..."+fileNameDownload) 
                #TODO : Find a way to get every downloaded file on chrome
                # and os.rename() to move it to our downloads folder.        
    def run(self):
        Spider = self.Spider
        # First of all, let's get all the needed data to start scrapping
        self.setData()
        
        ## DEBUG PURPOSES
        self.fillinYear("2017")
        self.selectOption(self.selects["c"],self.concours[4][1])
        self.selectOption(self.selects["f"],self.filieres[2][1])
        self.selectOption(self.selects["m"],self.matieres[0][1])

        self.submit() # Clicks "recherche button"
        self.getFiles()
        Spider.debugScreenShot()

#######
# Here you can define the procedure of you downloader
#######



