'''
---------------------
python 3
Author: mohabhui
Date: 24-Apr-2024
---------------------
'''

import custom_driver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import csv
import json
from types import SimpleNamespace
from selenium.webdriver.common.keys import Keys


#================================================== Config Section ===============================================
session_file = 'browser_session.txt'
pages_file = 'pages.json'
driver_path = r'.\webdriver\chromedriver.exe'  # Update this to your actual chromedriver path
driver = custom_driver.setup_driver(session_file, driver_path)
#====================================================xxx==================================================

# Recursive function to convert nested dictionaries to SimpleNamespace
def json_to_obj(data):
    if isinstance(data, dict):
        return SimpleNamespace(**{k: json_to_obj(v) for k, v in data.items()})
    elif isinstance(data, list):
        return [json_to_obj(item) for item in data]
    else:
        return data

# Load JSON and convert to SimpleNamespace
def load_pages(path):
    with open(path, 'r') as f:
        data = json.load(f)
        return json_to_obj(data)

#===================================== Common Pages Object ===============================================
pages = load_pages(pages_file)
#====================================================xxx==================================================

def fob(driver, locator):
    """
    fob --> find object
    Generic function to find an element based on type and locator.
    locator should be list e.g. ["XPATH", "//div[@id='utilityActionButtonElement/div/button/span[2]"]
    """
    loc_type = locator[0]
    loc = locator[1]
    if loc_type.upper() == "ID":
        return WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, loc)))
    elif loc_type.upper() == "XPATH":
        return WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, loc)))


def isPageExist(driver, pageUrl, locator):
    """
    Checks for the presence of a specific element after navigating to a URL.
    """
    try:
        driver.get(pageUrl)
        time.sleep(3)  # consider using WebDriverWait here instead for better reliability
        fob(driver, locator)
        return True
    except:
        return False

def toronto_utility_lookup(driver, csvFile, header=True):
    url = pages.toronto_utility.gen.url
    elm = pages.toronto_utility.elm # page elements

    with open(csvFile, newline='') as file:
        reader = csv.reader(file)
        if header:
            next(reader)  # Skip the header row

        for row in reader:
            driver.execute_script("window.open('');")  # Open a new tab
            driver.switch_to.window(driver.window_handles[-1])  # Switch to the new tab

            if isPageExist(driver, url, elm.terms_agree_button):
                terms_button = fob(driver, elm.terms_agree_button)
                terms_button.click()  # Click agree if the page and button are present

            time.sleep(5)  # Wait for any dynamic content to load

            account_input = fob(driver, elm.account_number_input)
            client_input = fob(driver, elm.client_number_input)
            last_name_input = fob(driver, elm.last_name_input)
            postal_input = fob(driver, elm.postal_code_input)
            payment_select = Select(fob(driver, elm.payment_method_select))
            submit_button = fob(driver, elm.submit_button)

            account_input.clear()
            account_input.send_keys(row[0])
            client_input.clear()
            client_input.send_keys(row[1])
            last_name_input.clear()
            last_name_input.send_keys(row[2])
            postal_input.clear()
            postal_input.send_keys(row[3])
            payment_select.select_by_visible_text(row[4])
##            submit_button.click()

            # Optionally close the tab if not needed anymore
            # driver.close()
            driver.switch_to.window(driver.window_handles[0])  # Switch back to the first tab




def tab_and_fill(driver, tab_num_arr, val_arr, start_elem_arr):
    '''
    This python selenium function first select and focus the start_elem_arr.
    The start_elem_arr will be like ["ID","ROLL_NUMBER"]. Then the function
    will iterate over tab_num_arr. For each integer in the tab_num_arr, that
    many tab will be send, after the tab, the element will be selected,
    focused, cleared and the value from val_arr at the same index of the
    tab_num_arr will be send. If the integer is 0, no tab will be send but
    the subsequent actions will be continued.
    '''

    # Resolve starting element
    start_by = getattr(By, start_elem_arr[0])  # Converts the string to a By type, e.g., By.ID
    start_value = start_elem_arr[1]            # The actual value to look for, e.g., "ROLL_NUMBER"

    # Focus on the starting element
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((start_by, start_value))
    )
    element.click()  # Focus by clicking

    # Iterate over the tab_num_arr and val_arr simultaneously
    for tab_count, value in zip(tab_num_arr, val_arr):
        # Send the required number of tab keys
        action = webdriver.ActionChains(driver)
        for _ in range(tab_count):
            action.send_keys(Keys.TAB)
        action.perform()

        # Now the focus should be on the target input element
        # Clear the input field before sending the value
        focused_elem = driver.switch_to.active_element
        focused_elem.clear()
        focused_elem.send_keys(value)




def toronto_property_tax_lookup(driver,csvFile, header=True):
    url = pages.toronto_prop_tax.gen.url
    elm = pages.toronto_prop_tax.elm # page elements
    with open(csvFile, newline='') as file:
        reader = csv.reader(file)
        if header:
            next(reader)  # Skip the header row

        for row in reader:
            driver.execute_script("window.open('');")  # Open a new tab
            driver.switch_to.window(driver.window_handles[-1])  # Switch to the new tab

            if isPageExist(driver, url, elm.terms_agree_button):
                terms_button = fob(driver, elm.terms_agree_button)
                terms_button.click()  # Click agree if the page and button are present

            time.sleep(3)  # Wait for any dynamic content to load

            # Assuming row contains [account_number, meter_number, last_name, postal_code, payment_method]

            tab_and_fill(driver, [0,1,2,2], [row[0], row[1], row[2], row[3]], ["ID","ROLL_NUMBER"])

            time.sleep(2)

##            fob(driver, elm.view_button).click()
##
##            time.sleep(2)

            # Optionally close the tab if not needed anymore
##            driver.close()
            driver.switch_to.window(driver.window_handles[0])  # Switch back to the first tab



if __name__ == '__main__':

##    toronto_utility_lookup(driver, "./data/utilityToronto.csv")
    toronto_property_tax_lookup(driver, "./data/propertyTaxToronto.csv")
