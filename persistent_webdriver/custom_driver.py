'''
---------------------
python 3
Author: mohabhui
Date: 24-Apr-2024
---------------------
'''

import os
import json
from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException

'''
You can close tab except the first tab or add tab to a
browser without loosing the session. If the first tab is closed,
the session will be lost and a new browser session will start.
'''

def create_driver_session(session_id, executor_url):
    from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
    org_command_execute = RemoteWebDriver.execute

    def new_command_execute(self, command, params=None):
        if command == "newSession":
            return {'success': 0, 'value': None, 'sessionId': session_id}
        else:
            return org_command_execute(self, command, params)
    RemoteWebDriver.execute = new_command_execute

    new_driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
    new_driver.session_id = session_id
    RemoteWebDriver.execute = org_command_execute
    return new_driver

def setup_driver(session_file, driver_path):
    try:
        if os.path.exists(session_file):
            with open(session_file, 'r') as file:
                session_data = json.load(file)
                driver = create_driver_session(session_data['session_id'], session_data['executor_url'])
                driver.get("https://www.google.com")  # Simple check to see if session is valid
                # Validate all windows and remove the closed ones from the session file
                open_windows = []
                for handle in driver.window_handles:
                    try:
                        driver.switch_to.window(handle)
                        open_windows.append(handle)
                    except NoSuchWindowException:
                        continue
                if not open_windows:  # All tabs were closed, open a new one
                    driver.execute_script("window.open('https://www.google.com');")
                    driver.switch_to.window(driver.window_handles[-1])
                    open_windows = [driver.current_window_handle]
                session_data['child_windows'] = open_windows
                with open(session_file, 'w') as file:
                    json.dump(session_data, file)
                return driver
    except Exception as e:
        print("Error with the saved session; Starting new session...")

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)
    session_info = {
        'session_id': driver.session_id,
        'executor_url': driver.command_executor._url,
        'parent_window': driver.current_window_handle,
        'child_windows': [driver.current_window_handle]
    }
    with open(session_file, 'w') as file:
        json.dump(session_info, file)
    return driver

if __name__ == "__main__":

    pass
