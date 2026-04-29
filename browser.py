"""CCIS Web Scraper Module

This module automates interaction with the CCIS web application using Selenium.
It handles login, juror search input, result navigation, and PDF generation
of case summary pages.

Core functionality includes:
- Initializing and configuring a Selenium WebDriver session
- Authenticating into the target website
- Submitting juror search criteria (name and date of birth)
- Navigating search results and selecting records
- Generating PDF snapshots of result pages via Chrome DevTools Protocol
- Saving PDF outputs to disk
- Resetting the application state for repeated queries

Typical usage flow:
1. Call `setup_browser()` to initialize and log in
2. Call `input_juror_data()` to perform a search
3. Call `select_view_selection()` to open the result
4. Call `generate_pdf_from_page()` to capture the page as a PDF
5. Call `save_pdf()` to persist the file
6. Call `return_to_main_page()` to reset for the next iteration
7. Call 'teardown_browser()' to close the browser

Dependencies:
- selenium (WebDriver automation)
- ChromeDriver (compatible with installed Chrome version)

Notes:
- driver and wait are passed explicitly as parameters to all functions that require them.
- Intended for automation workflows such as batch juror processing.
- Timing and element waits are managed using explicit waits and short delays.

Author: Nicholas Pham
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
from key import WEBSITE, CHROME_PATH, USERNAME, PASSWORD, TEST_FIRST_NAME, TEST_LAST_NAME, TEST_DATE_OF_BIRTH

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
def setup_browser() -> tuple:
    """
    Initializes the Selenium WebDriver, logs into the target website,
    and navigates to the main search page.

    The function:
    - Launches a Chrome browser instance
    - Navigates to the configured website
    - Logs in using provided credentials
    - Waits until the search page is fully loaded

    Returns:
        tuple[WebDriver, WebDriverWait]:
            A tuple containing:
            - driver: The active Selenium WebDriver instance
            - wait: WebDriverWait instance for handling explicit waits
    """
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

def input_juror_data(driver, wait, first_name, last_name, dob) -> None:
    """
    Inputs juror search criteria into the form and submits the search.

    The function:
    - Excludes attorneys and judges from the search
    - Fills in first name, last name, and date of birth
    - Clicks the search button to execute the query

    Args:
        first_name (str): Juror's first name
        last_name (str): Juror's last name
        dob (str): Juror's date of birth (expected format matches site input)

    Returns:
        None
    """
    driver.find_element(By.XPATH, EXCLUDE_ATTORNEYS_CHECKBOX_XPATH).click()
    driver.find_element(By.XPATH, EXCLUDE_JUDGES_CHECKBOX_XPATH).click()
    wait.until(EC.element_to_be_clickable((By.ID, LAST_NAME_FIELD_ID))).send_keys(last_name)  # finds username field enters username
    wait.until(EC.element_to_be_clickable((By.ID, FIRST_NAME_FIELD_ID))).send_keys(first_name)
    wait.until(EC.element_to_be_clickable((By.ID, DOB_FIELD_ID))).send_keys(dob)
    wait.until(EC.element_to_be_clickable((By.ID, SEARCH_BUTTON_ID))).click()

def select_view_selection(wait) -> None:
    """
    Clicks the 'View Selected' button on the search results page.

    This action navigates to the detailed case summary page
    for the selected record.

    Returns:
        None
    """
    wait.until(EC.element_to_be_clickable((By.ID, VIEW_SELECTION_BUTTON_ID))).click()

def generate_pdf_from_page(driver) -> bytes:
    """
    Generates a PDF of the current browser page using Chrome DevTools Protocol.

    The function:
    - Executes the 'Page.printToPDF' command via Selenium
    - Includes background graphics in the output
    - Decodes the returned base64 PDF data into raw bytes

    Returns:
        bytes: The generated PDF file as a byte object
    """
    pdf = driver.execute_cdp_cmd(PRINT_TO_PDF_WEBTOOL_COMMAND, {PRINT_BACKGROUND_KEY: True})
    return base64.b64decode(pdf[PDF_DATA_STRING])

def save_pdf(file_bytes, file_path):
    """
    Saves a PDF file to disk.

    Args:
        file_bytes (bytes): The PDF file data in bytes
        file_path (str): The full file path where the PDF will be saved

    Returns:
        None
    """
    with open(file_path, WRITE_BINARY_ACRONYM) as pdf_file:
        pdf_file.write(file_bytes)

def return_to_main_page(wait) -> None:
    """
    Navigates back to the main search page after viewing a case.

    The function:
    - Clicks the back button from the PDF view page
    - Clicks the back button from the selection page
    - Resets the search form
    - Waits briefly to ensure the page is fully reloaded

    Returns:
        None
    """
    wait.until(EC.element_to_be_clickable((By.ID, BACK_BUTTON_FROM_PDF_PAGE_ID))).click()
    wait.until(EC.element_to_be_clickable((By.ID, BACK_BUTTON_FROM_SELECTION_PAGE_ID))).click()
    wait.until(EC.element_to_be_clickable((By.ID, RESET_BUTTON_ID))).click()

    time.sleep(PAUSE_BETWEEN_ACTIONS_SECONDS)

def teardown_browser(driver) -> None:
    """
    Closes the browser and ends the WebDriver session.

    Args:
        driver: The active Selenium WebDriver instance

    Returns:
        None
    """
    driver.quit()

# TESTING ONLY
if __name__ == "__main__":
    driver, wait = setup_browser()
    input_juror_data(driver, wait, TEST_FIRST_NAME, TEST_LAST_NAME, TEST_DATE_OF_BIRTH)
    select_view_selection(wait)
    pdf_bytes = generate_pdf_from_page(driver)
    save_pdf(pdf_bytes, r"C:\Users\npham\PycharmProjects\venire_3.0\screenshots\ccis_output.pdf")
    return_to_main_page(wait)
    teardown_browser(driver)