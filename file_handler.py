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
        Filepath to the results folder ex: 'results/'
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
    Saves the last completed juror ID to progress.txt by writing to it so the program can resume if it crashes.

    Args:
        juror_id: The last completed juror ID ex: '1042'

    Returns:
        None
    """
    with open(PROGRESS_FILE, 'w') as progress_file:
        progress_file.write(str(juror_id))

def read_progress() -> str | None:
    """
    Reads the last completed juror ID from progress.txt.

    Returns:
        Last completed juror ID ex: '1042'
        None if no progress file exists yet
    """
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as progress_file:
            juror_id = progress_file.read().strip()
            return juror_id
    else:
        return None

def build_pdf_path(screenshot_folder: str, juror_id: str, last_name: str, first_name: str) -> str:
    """
    Builds the full file path for a juror's PDF.

    Args:
        screenshot_folder: Folder where screenshots are saved ex: 'screenshots/2025-04-23'
        juror_id:          Juror ID ex: '1042'
        last_name:         Juror last name ex: 'Smith'
        first_name:        Juror first name ex: 'John'

    Returns:
        Full path string ex: 'screenshots/2025-04-23/1042_Smith_John.pdf'
    """
    file_path = f"{juror_id}_{last_name}_{first_name}.pdf"
    return os.path.join(screenshot_folder, file_path)