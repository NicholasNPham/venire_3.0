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

def setup_folders() -> dict:
    """
    Runs at startup to create all required folders.

    Returns:
        Dictionary with folder paths ex: {'screenshots': 'screenshots/2025-04-23', 'results': 'results'}
    """
    screenshots_folder = create_screenshot_folder()
    results_folder = create_results_folder()

    print("SUCCESS: Loaded screenshots and results folders.")
    return {"screenshots": screenshots_folder, "results": results_folder}

def save_progress(juror_id: str) -> None:
    """
    Saves the last completed juror ID to progress.txt so the program can resume if it crashes.

    Args:
        juror_id: The last completed juror ID ex: '1042'

    Returns:
        None
    """
    with open(PROGRESS_FILE, 'w') as progress_file:
        progress_file.write(str(juror_id))
