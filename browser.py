"""
CCIS Web Scraper Module

This module automates interaction with the CCIS web application using Selenium.
It handles login, juror search input, result navigation, and PDF generation
of case summary pages.
"""

# Local Imports
from key import WEBSITE, CHROME_PATH, USERNAME, PASSWORD
from config import LoginConfig, SearchConfig, ResultsConfig, NavigationConfig, SecondsConfig

# Standard Library Imports
import time
import base64
import logging

# Third-party Imports
from selenium import webdriver # 4.43.0
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver

# CONSTANTS
PRINT_TO_PDF_WEBTOOL_COMMAND = "Page.printToPDF"
PDF_DATA_STRING = 'data'
PRINT_BACKGROUND_KEY = "printBackground"

# FUNCTIONS
def setup_browser(seconds_config: SecondsConfig) -> tuple:
    """
    Launches a Chrome browser instance and returns the driver and wait objects.

    The function:
    - Creates a Chrome WebDriver using the configured Chrome path
    - Initializes a WebDriverWait instance with the timeout from config

    Args:
        seconds_config (SecondsConfig): Dataclass containing timeout values

    Returns:
        tuple[WebDriver, WebDriverWait]:
            A tuple containing:
            - driver: The active Selenium WebDriver instance
            - wait: WebDriverWait instance for handling explicit waits

    Example:
        driver, wait = setup_browser(seconds_config)
    """
    service = Service(CHROME_PATH)
    driver = webdriver.Chrome(service=service)
    wait = WebDriverWait(driver, seconds_config.webdriver_wait_timeout)

    return driver, wait

def login(driver: WebDriver, wait: WebDriverWait, log: logging.Logger, login_config: LoginConfig, post_login_element_id: str ) -> None:
    """
    Navigates to the target website and logs in using stored credentials.

    The function:
    - Opens the configured website URL
    - Maximizes the browser window
    - Enters username and password from key.py
    - Submits the login form
    - Waits for the post-login element to confirm the search page loaded

    Args:
        driver (WebDriver): The active Selenium WebDriver instance
        wait (WebDriverWait): WebDriverWait instance for handling explicit waits
        log (logging.Logger): Logger instance for recording login status
        login_config (LoginConfig): Dataclass containing login form element IDs
        post_login_element_id (str): Element ID confirming successful login

    Returns:
        None

    Example:
        login(driver, wait, log, login_config, post_login_element_id)
    """
    # WEBSITE
    driver.get(WEBSITE)  # opens to the website.
    driver.maximize_window()  # maximizes the web driver
    log.info("Browser started successfully")
    # LOGIN
    wait.until(EC.element_to_be_clickable((By.ID, login_config.username_field))).send_keys(USERNAME)  # finds username field enters username
    wait.until(EC.element_to_be_clickable((By.ID, login_config.password_field))).send_keys(PASSWORD)  # finds password field and enters password
    driver.find_element(By.ID, login_config.submit_login_button).click()  # clicks submit to log in.
    wait.until(EC.presence_of_element_located((By.ID, post_login_element_id)))
    log.info("Logged in successfully")

def input_juror_data(driver, wait, first_name, last_name, dob, search_config: SearchConfig) -> None:

    """
    Inputs juror search criteria into the form and submits the search.

    The function:
    - Excludes attorneys and judges from the search
    - Fills in first name, last name, and date of birth
    - Clicks the search button to execute the query

    Args:
        driver (WebDriver): The active Selenium WebDriver instance
        wait (WebDriverWait): WebDriverWait instance for handling explicit waits
        first_name (str): Juror's first name
        last_name (str): Juror's last name
        dob (str): Juror's date of birth in mm/dd/yyyy format
        search_config (SearchConfig): Dataclass containing search form element IDs

    Returns:
        None

    Example:
        input_juror_data(driver, wait, "John", "Smith", "04/23/1985", search_config)
    """
    driver.find_element(By.XPATH, search_config.exclude_attorneys_checkbox).click()
    driver.find_element(By.XPATH, search_config.exclude_judges_checkbox).click()
    wait.until(EC.element_to_be_clickable((By.ID, search_config.last_name_field))).send_keys(last_name)  # finds username field enters username
    wait.until(EC.element_to_be_clickable((By.ID, search_config.first_name_field))).send_keys(first_name)
    wait.until(EC.element_to_be_clickable((By.ID, search_config.dob_field))).send_keys(dob)
    wait.until(EC.element_to_be_clickable((By.ID, search_config.search_button))).click()

def select_view_selection(wait, results_config: ResultsConfig) -> None:
    """
    Clicks the 'View Selected' button on the search results page.

    This action navigates to the detailed case summary page
    for the selected record.

    Args:
        wait (WebDriverWait): WebDriverWait instance for handling explicit waits
        results_config (ResultsConfig): Dataclass containing results page element IDs

    Returns:
        None

    Example:
        select_view_selection(wait, results_config)
    """
    wait.until(EC.element_to_be_clickable((By.ID, results_config.view_selection_button))).click()

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
    with open(file_path, "wb") as pdf_file:
        pdf_file.write(file_bytes)

def return_to_main_page(wait, navigation_config: NavigationConfig) -> None:
    """
    Navigates back to the main search page after viewing a case.

    The function:
    - Clicks the back button from the PDF view page
    - Clicks the back button from the selection page

    Args:
        wait (WebDriverWait): WebDriverWait instance for handling explicit waits
        navigation_config (NavigationConfig): Dataclass containing navigation element IDs

    Returns:
        None

    Example:
        return_to_main_page(wait, navigation_config)
    """
    wait.until(EC.element_to_be_clickable((By.ID, navigation_config.back_button_from_pdf_page))).click()
    wait.until(EC.element_to_be_clickable((By.ID, navigation_config.back_button_from_selection_page))).click()

def reset_search(wait, navigation_config: NavigationConfig, seconds_config: SecondsConfig) -> None:
    """
    Clicks the reset button to clear all search fields and return to a clean search state.

    The function:
    - Clicks the reset button on the search page
    - Waits briefly to ensure the page is fully reloaded before next action

    Args:
        wait (WebDriverWait): WebDriverWait instance for handling explicit waits
        navigation_config (NavigationConfig): Dataclass containing navigation element IDs
        seconds_config (SecondsConfig): Dataclass containing timeout values

    Returns:
        None

    Example:
        reset_search(wait, navigation_config, seconds_config)
    """
    wait.until(EC.element_to_be_clickable((By.ID, navigation_config.reset_button))).click()
    time.sleep(seconds_config.pause_between_actions)

def check_for_no_results(driver, log: logging.Logger, search_config: SearchConfig, seconds_config: SecondsConfig) -> bool:
    """
    Checks if the 'No matches found' popup appeared after a search.

    The function:
    - Creates a short-timeout wait to avoid blocking on missing elements
    - Returns True immediately if the no-results banner is visible
    - Returns False and logs a debug message if results are present

    Args:
        driver (WebDriver): The active Selenium WebDriver instance
        log (logging.Logger): Logger instance for recording search outcomes
        search_config (SearchConfig): Dataclass containing the no-results popup XPath
        seconds_config (SecondsConfig): Dataclass containing timeout values

    Returns:
        bool: True if no results found, False if results are present

    Example:
        is_empty = check_for_no_results(driver, log, search_config, seconds_config)
    """
    short_wait = WebDriverWait(driver, seconds_config.no_results_wait_timeout)

    try:
        short_wait.until(EC.visibility_of_element_located((By.XPATH, search_config.no_results_popup_message)))
        return True
    except Exception:
        log.debug("No 'No Results Found' Prompt, Navigating to Results Page")
        return False

def teardown_browser(driver, log: logging.Logger) -> None:
    """
    Closes the browser and ends the WebDriver session.

    Args:
        driver: The active Selenium WebDriver instance
        log (logging.Logger): Logger instance for recording search outcomes

    Returns:
        None
    """
    log.info("FINISHED VENIRE EXCEL")
    driver.quit()

