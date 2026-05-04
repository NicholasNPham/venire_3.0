"""
File: logger.py
Purpose: Configures and returns the logger for Venire Automation
"""

# STANDARD LIBRARY IMPORTS
import logging
import os
from datetime import date

# CONSTANTS
RESULTS_ROOT = 'results'
LOG_FILE = os.path.join(RESULTS_ROOT, date.today().strftime('%Y-%m-%d')) + '.log'

# FUNCTIONS

def setup_logger() -> logging.Logger:
    pass

