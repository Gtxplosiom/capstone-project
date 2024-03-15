from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class BrowserStuff:
    def __init__(self):
        self.options = Options()
        self.options.add_experimental_option("detach", True) #this make the browser do not close when script is done 'scripting'

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
    
    def open_google(self):
        self.driver.get("https://www.google.com/")
        self.driver.maximize_window()

        self.find_element("Gmail")

    def find_element(self, element: str):
        links = self.driver.find_elements("xpath", "//a[@href]")
        for link in links:
            if element in link.get_attribute("innerHTML"):
                link.click()
                break

chrome = BrowserStuff()
chrome.open_google()