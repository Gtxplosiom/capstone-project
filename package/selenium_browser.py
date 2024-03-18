from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class SeleniumBrowser:

    browser_is_active = False
    
    def __init__(self):

        self.user_data_dir = 'C:/Users/admin/AppData/Local/Google/Chrome/User Data/'

        self.options = Options()
        self.options.add_experimental_option('detach', True)    # this makes the browser not close when the script is done 'scripting'
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.options.add_argument(f'--user-data-dir={self.user_data_dir}')
        self.options.add_argument(r'--profile-directory=Profile 4')

        self.symbols = ['!', ',', '.', '?']

    def open_browser(self):
        self.browser_is_active = True

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
        self.driver.get('https://www.google.com/')
        self.driver.maximize_window()

    def close_browser(self):
        self.driver.quit()
        
    def search(self, query: str):
        search_box = self.driver.find_element('name', 'q')    # for actual chrome search text bar, not the address bar.
        search_box.clear()
        search_box.send_keys(query)
        search_box.submit()

    def scroll(self, direction: str, amount: int):
        if direction == 'up':
            self.driver.execute_script(f"window.scrollTo(0, -{amount});")
        elif direction == 'down':
            self.driver.execute_script(f"window.scrollTo(0, {amount});")
        else:
            pass

    def execute_in_browser(self, asr_string: str):
        split_string = asr_string.split()

        if len(split_string) > 0:

            command = split_string[0]
            command = command.capitalize()
            for x in self.symbols:
                command = command.replace(x, '')

            query = split_string[1:]
            query = ' '.join(query)
            for x in self.symbols:
                query = query.replace(x, '')

            print(command)
            print(query)

            if command == 'Open' and query == 'browser':
                self.open_browser()
            elif command == "Close" and query == 'browser':
                self.browser_is_active = False
                self.close_browser()
            elif command == 'Search':
                self.search(query)
            elif command == 'Scroll':
                self.scroll(query, 500)
            else:
                pass
        else:
            pass