import datetime
import os
from typing import Union
from xml.etree import ElementTree as Et


class Tasks:
    def __init__(self, difference: int, future: Union[datetime.datetime, None] = None):
        # HHClick and HHClickSleep
        self.name = 'HHClicker'
        self.name_sleep = self.name + 'Sleep'
        self.name_startup = self.name + 'Startup'
        self.difference = difference
        self.future = future
        self.root_dir = os.path.dirname(os.path.abspath(__file__))

        self.xml_url = '{http://schemas.microsoft.com/windows/2004/02/mit/task}'

        # names of files with path to hhclick. Example: \\path\\to\\here\\HHClick.xml
        self.xml_file = self.root_dir + '\\' + self.name + '.xml'
        self.xml_file_slept = self.root_dir + '\\' + self.name_sleep + '.xml'
        self.xml_file_startup = self.root_dir + '\\' + self.name_startup + '.xml'

    def __change_user_and_path(self, tree):
        tree.find(f'{self.xml_url}Actions/{self.xml_url}Exec/{self.xml_url}Command').text = self.root_dir + '\\main.py' # исполняемый файл
        tree.find(f'{self.xml_url}RegistrationInfo/{self.xml_url}Author').text = os.getlogin() #от чьего имени

    def __change_idle_xml(self):
        tree = Et.parse(self.xml_file)
        future_xml_date = self.future.strftime('%Y-%m-%dT%H:%M:%S')
        tree.find(
            f'{self.xml_url}Triggers/{self.xml_url}TimeTrigger/{self.xml_url}StartBoundary').text = future_xml_date # когда запустить файл
        self.__change_user_and_path(tree)
        tree.write(self.xml_file)

    def __change_sleep_xml(self):
        tree = Et.parse(self.xml_file_slept)
        self.future += datetime.timedelta(seconds=self.difference)
        future_xml_date = self.future.strftime('%Y-%m-%dT%H:%M:%S')
        tree.find(
            f'{self.xml_url}Triggers/{self.xml_url}TimeTrigger/{self.xml_url}StartBoundary').text = future_xml_date
        self.__change_user_and_path(tree)
        tree.write(self.xml_file_slept)

    def __change_startup_xml(self):
        tree = Et.parse(self.xml_file_startup)
        self.__change_user_and_path(tree)
        tree.write(self.xml_file_startup)

    def change_xmls(self):
        if not self.future:
            self.future = datetime.datetime.now() + datetime.timedelta(hours=4)
        self.__change_idle_xml()
        self.__change_sleep_xml()
        self.__change_startup_xml()

    def create_tasks(self):
        self.change_xmls()
        # будущий запуск
        command = f"SCHTASKS /CREATE /tn {self.name} /XML {self.xml_file} /F"
        os.system(command)
        command = f"SCHTASKS /CREATE /tn {self.name_sleep} /XML {self.xml_file_slept} /F"
        os.system(command)
        command = f"SCHTASKS /CREATE /tn {self.name_startup} /XML {self.xml_file_startup} /F"
        os.system(command)

    def uninstall(self):
        # будущий запуск
        command = f"SCHTASKS /DELETE /tn {self.name}"
        os.system(command)
        command = f"SCHTASKS /DELETE /tn {self.name_sleep}"
        os.system(command)
        command = f"SCHTASKS /DELETE /tn {self.name_startup}"
        os.system(command)


