"""
File: main.py
Purpose: Main loop for Venire Automation
"""

# LOCAL IMPORTS
from browser import setup_browser, login, input_juror_data, check_for_no_results, select_view_selection, generate_pdf_from_page, save_pdf, return_to_main_page, reset_search, teardown_browser
from excel_handler import load_jurors, write_outcome, bulk_write_error_outcome
from file_handler import setup_folders, build_pdf_path, save_progress, read_progress, delete_progress
from report_builder import prompt_and_combine, combine
from logger import setup_logger
from config import load_config
from cli import parse_args

# STANDARD LIBRARY IMPORTS
import os
from datetime import date

# CONSTANT
JSON_FILE: str = "config.json"

# FUNCTIONS
def main():
    """
    Entry point for Venire Automation 3.0.

    Orchestrates the full juror processing pipeline from setup to teardown.

    The function:
    - Parses CLI arguments for headless mode, row limits, and combine behavior
    - Sets up output folders, structured logging, and config from config.json
    - Loads jurors from Excel and launches a Chrome browser session
    - Resumes from last completed juror if a progress file exists
    - For each juror: searches, checks for results, generates a PDF if found,
      and writes the outcome back to Excel
    - Flags compound last names with no results for manual review
    - On completion, optionally merges all PDFs and the Excel report into one file

    Args:
        None

    Returns:
        None

    Example:
        python main.py
        python main.py --headless --limit 10 --no-combine
    """
    args = parse_args()

    # SETUP - RUN ONCE
    folders = setup_folders()

    # SETUP - LOG FILES
    log_path = os.path.join(folders["screenshots"], f"{date.today().strftime('%Y-%m-%d')}.log")
    log = setup_logger(log_path)

    # SETUP - CONFIG JSON FILE
    config = load_config(JSON_FILE)

    # SETUP - RUN ONCE
    jurors = load_jurors(config.app.excel_file, log, config.app.outcome_bad_format)
    log.info("Folders and jurors loaded successfully")

    # SETUP - BROWSER -> LOGIN
    driver, wait = setup_browser(config.browser.seconds, args.headless)
    login(driver, wait, log, config.browser.login, config.browser.search.last_name_field)

    # RESUME LOGIC - CHECK IF PROGRESS FILE EXIST
    last_completed = None # Always initialize last_completed as None
    skip = False

    if not args.fresh:
        last_completed = read_progress()
        skip = last_completed is not None

    # SET DEFAULT OUTCOME FOR ALL JURORS BEFORE LOOP STARTS
    if not skip:
      bulk_write_error_outcome(config.app.excel_file, jurors, config.app.outcome_error, log)

    # MAIN LOOP
    completed = False
    try:
        for i, (juror_id, data) in enumerate(jurors.items(), start=1):

            # This arg will check if --limit is not none and checks to see if 'i' is greater than args.limit
            if args.limit is not None and i >= args.limit:
                break

            # SKIP UNTIL WE PASS LAST COMPLETED
            if skip:
                if juror_id == last_completed:
                    skip = False
                continue

            try:
                log.info(f"{i}/{len(jurors)}")
                input_juror_data(driver, wait, data['first_name'], data['last_name'], data['dob'], config.browser.search) # SEARCH
                is_no_result_found = check_for_no_results(driver, log, config.browser.search, config.browser.seconds) # CHECK FOR NO RESULTS
                # IF NO RESULTS — write outcome, reset, next juror
                if is_no_result_found:
                    if len(data["last_name"].split()) >= 2:
                        outcome = config.app.outcome_bad_format
                        log.warning(f"Juror ID: {juror_id} - found compound last name - flagged for manual review")
                    else:
                        outcome = config.app.outcome_no_results
                    write_outcome(config.app.excel_file, data['row'], outcome)
                    save_progress(juror_id)
                    reset_search(wait, config.browser.navigation, config.browser.seconds)
                    continue
                # IF RESULTS — select, generate pdf, save pdf, write outcome
                else:
                    select_view_selection(wait, config.browser.results, config.browser.navigation)
                    pdf_bytes = generate_pdf_from_page(driver)
                    pdf_path = build_pdf_path(folders["screenshots"], juror_id, data["last_name"], data["first_name"])
                    save_pdf(pdf_bytes, pdf_path)
                    write_outcome(config.app.excel_file, data["row"], config.app.outcome_complete)
                    return_to_main_page(wait, config.browser.navigation)
                    save_progress(juror_id)
                    reset_search(wait, config.browser.navigation, config.browser.seconds)

            except Exception as e:
                log.error(f"Error on juror {juror_id}: {e}")
                write_outcome(config.app.excel_file, data["row"], config.app.outcome_error)
                try:
                    reset_search(wait, config.browser.navigation, config.browser.seconds)
                except Exception as error:
                    log.error(f"Reset failed after error — breaking out of loop. - {error}")
                    break
                continue

        else:
            completed = True

    finally:
        if completed:
            delete_progress()
        teardown_browser(driver, log) # ALWAYS RUN NO MATTER WHAT

    if args.combine is None and completed:
        prompt_and_combine(folders["screenshots"], config.app.excel_file, log)
    elif args.combine is True and completed:
        combine(folders["screenshots"], config.app.excel_file, log)
    elif args.combine is False and completed:
        log.info("Skipping PDF combine — --no-combine passed.")

if __name__ == "__main__":
    main()