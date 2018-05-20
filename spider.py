from crawler import Crawler

# Import Selenium modules
from selenium import webdriver
from selenium.webdriver.support.select import Select


class MathUPSpider():
    
    concours = []
    filieres = []
    matieres = []
    selects = {
        "c":"concours",
        "m":"matiere",
        "f":"filiere"
    }

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

    def initVisit(self):
        """ Opens up the search form """
        Spider = self.Spider
        Spider.launchBrowser(True)
        Spider.goToSite()
        self.clickButton("commande") # Clicks "connexion button"
        Spider.wait()

    def setData(self):
        """ Fetches concours,filiers,matieres from the search form"""
        self.initVisit()
        self.concours = self.getSelectValues(self.selects["c"])
        self.filieres = self.getSelectValues(self.selects["f"])
        self.matieres = self.getSelectValues(self.selects["m"])

    def run(self):
        # First of all, let's get all the needed data to start scrapping
        Spider = self.Spider
        self.setData()
        print(self)    

        #self.selectOption("concours",concours[2][1])
        #self.clickButton("commande") # Clicks "recherche button"
        #Spider.debugScreenShot()

#######
# Here you can define the procedure of you downloader
#######



