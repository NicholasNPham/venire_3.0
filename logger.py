"""
File: logger.py
Purpose: Configures and returns the logger for Venire Automation
"""

# STANDARD LIBRARY IMPORTS
import logging
import sys

# CONSTANTS


# FUNCTIONS
def setup_logger(log_path: str) -> logging.Logger:
    """
    Configures and returns the Venire logger with a file handler and console handler.
    Calling this function more than once returns the existing logger without adding
    duplicate handlers.

    Args:
        log_path (str): Full path to the log file, e.g. 'results/2026-05-05/2026-05-05.log'

    Returns:
        logging.Logger: Configured logger named 'Venire' with DEBUG level enabled.

    Examples:
        logger = setup_logger('results/2026-05-05/2026-05-05.log')
        logger.info('Starting Venire Automation')
        2026-05-05 10:32:11 - Venire - INFO - Starting Venire Automation
    """
    logger = logging.getLogger('Venire')
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Create File Handler
    file_handler = logging.FileHandler(log_path)
    file_handler.setFormatter(formatter)

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # Attach both handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
