from main import HHClicker
from selenium.webdriver.firefox.options import Options


def obtain_cookies(obj):
    obj.get(obj.url_main)
    answer = ''
    while answer != 'done':
        answer = input('Пройди авторизацию в браузере. Когда закончишь, напиши "done": ')
    result = obj.get_cookies()
    with open('cookies.txt', 'w') as file:
        file.write(result.__str__())


if __name__ == '__main__':
    with HHClicker() as hh:
        obtain_cookies(hh)
