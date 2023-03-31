from selenium.webdriver import Firefox
import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from Tasks import Tasks
import ast
import os


class HHClicker(Firefox):
    url_main = 'https://spb.hh.ru/account/login?backurl=%2F&hhtmFrom=main'
    summary_url = 'https://spb.hh.ru/applicant/resumes'

    def __init__(self):
        self.difference = 200  # разница между активным режимом и спящим (в сек)
        self.cookies = self.get_cookies_from_file()
        super().__init__(service=Service(log_path='NUL'))

    @staticmethod
    def __get_future(element):
        text = element.text.split()
        now = datetime.datetime.now()
        hour, minute = map(int, text[-1].split(':'))
        if text[-3] == 'сегодня':
            future = datetime.datetime(year=now.year, month=now.month, day=now.day, hour=hour, minute=minute)
        else:
            buf = now + datetime.timedelta(days=1)
            future = datetime.datetime(year=buf.year, month=buf.month, day=buf.day, hour=hour, minute=minute)
        return future + datetime.timedelta(minutes=1) # запас в минуту

    def __create_tasks(self):
        elements = self.find_elements(By.CLASS_NAME, "applicant-resumes-action_second")
        buffer = None
        for el in elements:
            future = self.__get_future(el)
            if not buffer:
                buffer = future
            elif buffer < future:
                buffer = future

        self.close()
        print('Creating tasks...')
        tasks = Tasks(self.difference, buffer)
        tasks.create_tasks()

    def insert_cookies(self):
        print('Opening browser...')
        self.get(self.url_main)
        self.delete_all_cookies()
        for c in self.cookies:
            self.add_cookie(c)

    @staticmethod
    def get_cookies_from_file():
        try:
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cookies.txt')) as cookies:
                result = ast.literal_eval(cookies.read())
                if isinstance(result, list):
                    for c in result:
                        if not isinstance(c, dict):
                            exit('Not valid cookies!')
                    return result
                else:
                    exit('Not valid cookies!')
        except SyntaxError:
            exit('Empty cookies.py, run obtain_cookies.py first!')
        except FileNotFoundError:
            exit("Can't find cookies.txt")

    def auth_complete(self):
        if self.current_url == self.summary_url:
            return True
        return False

    def run(self):
        try:
            self.insert_cookies() # вставить куки
            self.get(self.summary_url)
            if not self.auth_complete():
                exit('Please, update cookies!')
            buttons = self.find_elements(By.XPATH,'//button[@class="bloko-link"][@type="button"][@data-qa="resume-update-button_actions"]')
            for button in buttons:
                if button.text == 'Поднять в поиске':
                    button.click()
            self.__create_tasks()
        except Exception as e:
            print(e.__str__())
            exit('Че-то пошло не так в run')
