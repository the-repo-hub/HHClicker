It is automatic clicker for promotion your summary on https://hh.ru

THIS APP WORKS WITH WINDOWS ONLY!!!

What does the app do?
Opens the browser on the summary page, looks for the raise button in the search and clicks it. Then he creates a task in the task manager for self-execution in about 4 hours. The application takes the execution time from the browser. 3 tasks are created (XML files in the directory):
1. "Active" task: just executes the program and creates a new task
2. "Sleepy" task: wakes up the computer from sleep and exits by putting it to sleep. This task will only run during sleep and is delayed by 200 seconds compared to "active" to allow it to run earlier and not fall asleep during active work
3. Task at startup, which is always executed at startup, to update the data.


INSTRUCTION:

How to run the application correctly?

First of all, you need to run the obtain_cookies.py script and go through authorization in the browser. After passing the authorization, it is necessary NOT to close the browser to write "don" in the console window that opens with the browser. This way the script will get your cookies.

Then you need to run the main.py script STRICTLY AS ADMINISTRATOR, otherwise you will have problems creating tasks, especially those that control sleep.

And that's it, the application will work.

How to stop the application and delete it?
To delete the script, you need to delete 3 tasks in the task scheduler:

1. HHClicker
2. HHClickerSleep
3. HHClickerStartup

And that's it, the app won't work anymore.
