import datetime
from HH import HHClicker
import argparse
import os
from selenium.common.exceptions import WebDriverException
from Tasks import Tasks


def main():
    try:
        print('Starting...\n')

        parser = argparse.ArgumentParser()
        group = parser.add_mutually_exclusive_group()

        group.add_argument('--sleep', help='sleep after execution', action='store_true')
        group.add_argument('-d', help='set difference between active and sleep xml')
        args = parser.parse_args()
        Tasks.delete_tasks()

        while True:
            try:
                with HHClicker() as hh:
                    hh.run()
                    break
            except WebDriverException:
                pass

        if args.sleep:
            # заснуть
            command = "powercfg -hibernate off  &&  start /min %windir%\System32\\rundll32.exe powrprof.dll,SetSuspendState Standby  &&  ping -n 3 127.0.0.1  &&  powercfg -hibernate on"
            os.system(command)

    except KeyboardInterrupt:
        exit('Bye!')


if __name__ == '__main__':
    start_time = datetime.datetime.now()
    main()
    print(f'Время выполнения: {datetime.datetime.now() - start_time}')
