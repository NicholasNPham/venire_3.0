"""
File: excel_handler.py
Purpose: Handles all Excel read and write operations for Venire Automation
"""

# Standard Library Imports
import os

# Third-Party Library Imports
import openpyxl # 3.1.5

# CONSTANTS
NAME_COLUMN = 3
DOB_COLUMN = 2
JUROR_COLUMN = 1
OUTCOME_COLUMN = 4

# PARSE CONSTANTS
MAX_SPLIT_PARAMETER = 1
FIRST_NAME_SPLIT_PARAMETER = 0
COMMA_DELIMITER = ","

# FUNCTIONS
def load_workbook_safe(file_path: str):
    if not os.path.exists(file_path): # If the file path does not exist is not there.
        raise FileNotFoundError(f"File not found: {file_path}") # Raise an error if the Excel sheet cannot be found.
    return openpyxl.load_workbook(file_path) # Return the open Excel sheet if it is found.

def parse(name: str)-> tuple:
    if not name or "," not in name: # Checks to if the name is empty or does not have a comma
        return None, None # If empty or does not have a comma return None, None

    left, right = name.split(COMMA_DELIMITER, MAX_SPLIT_PARAMETER) # Split the name by the comma and at the first comma it sees.

    last_name = left.strip() # Removes whitespace
    right = right.strip() # Removes whitespace with the first
    if not right:
        return None, None

    first_name = right.split()[FIRST_NAME_SPLIT_PARAMETER] # This takes the first half of the two names.

    return first_name, last_name
