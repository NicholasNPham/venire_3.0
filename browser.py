"""
CCIS Web Scraper Module

"""

# Standard Library Imports
import time
import base64

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
WRITE_BINARY_ACRONYM = "wb"
PRINT_TO_PDF_WEBTOOL_COMMAND = "Page.printToPDF"
PDF_DATA_STRING = 'data'
PRINT_BACKGROUND_KEY = "printBackground"

# HTML CONSTANTS
USERNAME_FIELD_ID = "loginForm:username"
PASSWORD_FIELD_ID = "loginForm:password"
SUBMIT_LOGIN_BUTTON_ID = "loginForm:login"

EXCLUDE_ATTORNEYS_CHECKBOX_XPATH = "//label[@for='search_tab:personForm:nameTypes:0']"
EXCLUDE_JUDGES_CHECKBOX_XPATH = "//label[@for='search_tab:personForm:nameTypes:1']"
LAST_NAME_FIELD_ID = "search_tab:personForm:lastname"
FIRST_NAME_FIELD_ID = "search_tab:personForm:fname"
DOB_FIELD_ID = "search_tab:personForm:dob_input"
SEARCH_BUTTON_ID = "search_tab:personForm:j_idt158"

VIEW_SELECTION_BUTTON_ID = "searchPartyResults:viewSelectedButton"

BACK_BUTTON_FROM_PDF_PAGE_ID = "caseSummary:j_idt114"
BACK_BUTTON_FROM_SELECTION_PAGE_ID = "j_idt111"
RESET_BUTTON_ID = "search_tab:personForm:j_idt159"

# FUNCTIONS
def setup_browser():
    service = Service(CHROME_PATH)
    driver = webdriver.Chrome(service=service)
    wait = WebDriverWait(driver, WEBDRIVER_WAIT_TIMEOUT_SECONDS)
    driver.get(WEBSITE) # opens to the website.
    driver.maximize_window() # maximizes the web driver
    # LOGIN PATH
    wait.until(EC.element_to_be_clickable((By.ID, USERNAME_FIELD_ID))).send_keys(USERNAME) # finds username field enters username
    wait.until(EC.element_to_be_clickable((By.ID, PASSWORD_FIELD_ID))).send_keys(PASSWORD) # finds password field and enters password
    driver.find_element(By.ID, SUBMIT_LOGIN_BUTTON_ID).click() # clicks submit to log in.
    wait.until(EC.presence_of_element_located((By.ID, LAST_NAME_FIELD_ID)))

    return (driver, wait)

def input_juror_data(driver, wait, first_name, last_name, dob):
    driver.find_element(By.XPATH, EXCLUDE_ATTORNEYS_CHECKBOX_XPATH).click()
    driver.find_element(By.XPATH, EXCLUDE_JUDGES_CHECKBOX_XPATH).click()
    wait.until(EC.element_to_be_clickable((By.ID, LAST_NAME_FIELD_ID))).send_keys(last_name)  # finds username field enters username
    wait.until(EC.element_to_be_clickable((By.ID, FIRST_NAME_FIELD_ID))).send_keys(first_name)
    wait.until(EC.element_to_be_clickable((By.ID, DOB_FIELD_ID))).send_keys(dob)
    wait.until(EC.element_to_be_clickable((By.ID, SEARCH_BUTTON_ID))).click()

    return (driver, wait)

def select_view_selection(driver, wait):
    wait.until(EC.element_to_be_clickable((By.ID, VIEW_SELECTION_BUTTON_ID))).click()

    return (driver, wait)

def generate_pdf_from_page(driver):
    pdf = driver.execute_cdp_cmd(PRINT_TO_PDF_WEBTOOL_COMMAND, {PRINT_BACKGROUND_KEY: True})
    return base64.b64decode(pdf[PDF_DATA_STRING])

def save_pdf(file_bytes, file_path):
    with open(file_path, WRITE_BINARY_ACRONYM) as pdf_file:
        pdf_file.write(file_bytes)

def return_to_main_page(driver, wait):
    wait.until(EC.element_to_be_clickable((By.ID, BACK_BUTTON_FROM_PDF_PAGE_ID))).click()
    wait.until(EC.element_to_be_clickable((By.ID, BACK_BUTTON_FROM_SELECTION_PAGE_ID))).click()
    wait.until(EC.element_to_be_clickable((By.ID, RESET_BUTTON_ID))).click()

    time.sleep(WEBDRIVER_WAIT_TIMEOUT_SECONDS)

    return (driver, wait)



# TESTING ONLY
driver, wait = setup_browser()
input_juror_data(driver, wait, TEST_FIRST_NAME, TEST_LAST_NAME, TEST_DATE_OF_BIRTH)
select_view_selection(driver, wait)
pdf_bytes = generate_pdf_from_page(driver)
save_pdf(pdf_bytes, r"C:\Users\npham\PycharmProjects\venire_3.0\screenshots\ccis_output.pdf")
return_to_main_page(driver, wait)