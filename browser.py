"""
CCIS Web Scraper Module

"""

# Standard Library Imports
import time

# Third-party Imports
from selenium import webdriver # 4.43.0
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Local Imports
from key import *

# CONSTANTS
PAUSE_BETWEEN_ACTIONS_SECONDS = 1
WEBDRIVER_WAIT_TIMEOUT_SECONDS = 5

# HTML CONSTANTS
USERNAME_FIELD_ID = "loginForm:username"
PASSWORD_FIELD_ID = "loginForm:password"
SUBMIT_LOGIN_BUTTON_ID = "loginForm:login"
EXCLUDE_ATTORNEYS_CHECKBOX_ID = "search_tab:personForm:nameTypes:0"
EXCLUDE_JUDGES_CHECKBOX_ID    = "search_tab:personForm:nameTypes:1"
LAST_NAME_FIELD_ID = "search_tab:personForm:lastname"
FIRST_NAME_FIELD_ID = "search_tab:personForm:fname"
DOB_FIELD_ID = "search_tab:personForm:dob_input"
SEARCH_BUTTON_ID = "search_tab:personForm:j_idt158"

# FUNCTIONS
def setup_browser():
    """Open Chrome, log in to STAC website, and wait for the sidebar.

    Returns:
        tuple (WebDriver, WebDriverWait): Initialized driver and wait object.

    Raises:
        WebDriverException: If Chrome or chromedriver fails to launch.
        TimeoutException: If the sidebar element does not appear after login.
    """
    # DRIVER SET-UP
    service = Service(CHROME_PATH)
    driver = webdriver.Chrome(service=service)
    wait = WebDriverWait(driver, WEBDRIVER_WAIT_TIMEOUT_SECONDS)
    driver.get(WEBSITE) # opens to the website.
    driver.maximize_window() # maximizes the web driver
    # LOGIN PATH
    wait.until(EC.element_to_be_clickable((By.ID, USERNAME_FIELD_ID))).send_keys(USERNAME) # finds username field enters username
    wait.until(EC.element_to_be_clickable((By.ID, PASSWORD_FIELD_ID))).send_keys(PASSWORD) # finds password field and enters password
    driver.find_element(By.ID, SUBMIT_LOGIN_BUTTON_ID).click() # clicks submit to log in.

    return (driver, wait)

def input_juror_data(driver, wait, first_name, last_name, dob):
    wait.until(EC.element_to_be_clickable((By.ID, LAST_NAME_FIELD_ID))).send_keys()  # finds username field enters username
    wait.until(EC.element_to_be_clickable((By.ID, FIRST_NAME_FIELD_ID))).send_keys(PASSWORD)

setup_browser()