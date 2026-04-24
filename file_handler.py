"""
File: file_handler.py
Purpose: Handles folder creation, progress tracking, and file paths for Venire Automation
"""

# STANDARD LIBRARY IMPORTS
import os
from datetime import date

# CONSTANTS
SCREENSHOTS_ROOT = 'screenshots'
RESULTS_ROOT = 'results'
PROGRESS_FILE = os.path.join(RESULTS_ROOT, 'progress.txt')

# FUNCTIONS
def get_date_folder() -> str:
    """
    Returns today's date as a string for folder naming.

    Returns:
        Date string ex: '2025-04-23'
    """
    return str(date.today())

def create_screenshot_folder() -> str:
    """
    Returns the filepath for the screenshot folder and makes the folder and checks to see if the folder exists.

    Returns:
        Filepath to the screenshot folder ex: 'screenshots/2025-04-23'
    """
    filepath_to_screenshot = os.path.join(SCREENSHOTS_ROOT, get_date_folder())
    os.makedirs(filepath_to_screenshot, exist_ok=True)
    return filepath_to_screenshot

def create_results_folder() -> str:
    """
    Returns the filepath for the results folder and makes the folder and checks to see if the folder exists.

    Returns:
        Filepath to the screenshot folder ex: 'results/'
    """
    os.makedirs(RESULTS_ROOT, exist_ok=True)
    return RESULTS_ROOT

