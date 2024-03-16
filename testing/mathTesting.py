from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

class BrowserStuff:
    def __init__(self):
        self.user_data_dir = 'C:/Users/admin/AppData/Local/Google/Chrome/User Data/'

        self.options = Options()
        self.options.add_experimental_option('detach', True)    # this makes the browser not close when the script is done 'scripting'
        self.options.add_experimental_option('excludeSwitches', 'enable-automation')
        self.options.add_argument(f'--user-data-dir={self.user_data_dir}')
        self.options.add_argument(r'--profile-directory=Profile 4')

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)

    def open_google(self):
        self.driver.get('https://www.google.com/')
        self.driver.maximize_window()
        
    def search(self, query: str):
        search_box = self.driver.find_element('name', 'q')    # for actual chrome search text bar, not the address bar.
        search_box.clear()
        search_box.send_keys(query)
        search_box.submit()

class ProxyASR:
    def __init__(self):
        self.browser = BrowserStuff()

    def execute(self, command: str):
        command = command.split()

        query = command[1:]
        query = ' '.join(query)

        command = command[0]

        if command == 'Open' and query == 'browser':
            self.browser.open_google()
        elif command == 'Search':
            self.browser.search(query)

asr = ProxyASR()

asr.execute('Open browser')

time.sleep(3)

asr.execute('Search how to remove selenium chrome is being handles by test software')