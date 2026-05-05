"""
File: main.py
Purpose: Main loop for Venire Automation
"""

# LOCAL IMPORTS
from browser import setup_browser, input_juror_data, check_for_no_results, select_view_selection, generate_pdf_from_page, save_pdf, return_to_main_page, reset_search, teardown_browser
from excel_handler import load_jurors, write_outcome
from file_handler import setup_folders, build_pdf_path, save_progress, read_progress, delete_progress
from report_builder import prompt_and_combine
from logger import setup_logger

# STANDARD LIBRARY IMPORTS
import os
from datetime import date

# CONSTANT
EXCEL_FILE = "VENIRE.xlsx"

# OUTCOME CONSTANTS
OUTCOME_NO_RESULTS = "No matches found"
OUTCOME_COMPLETE   = "CH Found"
OUTCOME_ERROR      = "Error - check manually"

# FUNCTIONS
def main():

    # SETUP - RUN ONCE
    folders = setup_folders()

    # LOG FILES - SETUP
    log_path = os.path.join(folders["screenshots"], f"{date.today().strftime('%Y-%m-%d')}.log")
    log = setup_logger(log_path)

    # SETUP - RUN ONCE
    jurors = load_jurors(EXCEL_FILE, log)
    log.info("Folders and jurors loaded successfully")

    # SETUP - BROWSER
    driver, wait = setup_browser(log)

    # SET DEFAULT OUTCOME FOR ALL JURORS BEFORE LOOP STARTS
    for juror_id, data in jurors.items():
        write_outcome(EXCEL_FILE, data["row"], OUTCOME_ERROR)

    # RESUME LOGIC - CHECK IF PROGRESS FILE EXIST
    last_completed = read_progress()
    skip = last_completed is not None


    # MAIN LOOP
    completed = False
    try:
        for i, (juror_id, data) in enumerate(jurors.items(), start=1):

            # SKIP UNTIL WE PASS LAST COMPLETED
            if skip:
                if juror_id == last_completed:
                    skip = False
                continue

            try:
                log.info(f"{i}/{len(jurors)}")
                input_juror_data(driver, wait, data['first_name'], data['last_name'], data['dob']) # SEARCH
                is_no_result_found = check_for_no_results(driver, log) # CHECK FOR NO RESULTS
                # IF NO RESULTS — write outcome, reset, next juror
                if is_no_result_found:
                    write_outcome(EXCEL_FILE, data['row'],OUTCOME_NO_RESULTS)
                    reset_search(wait)
                    continue
                # IF RESULTS — select, generate pdf, save pdf, write outcome
                else:
                    select_view_selection(wait)
                    pdf_bytes = generate_pdf_from_page(driver)
                    pdf_path = build_pdf_path(folders["screenshots"], juror_id, data["last_name"], data["first_name"])
                    save_pdf(pdf_bytes, pdf_path)
                    write_outcome(EXCEL_FILE, data["row"], OUTCOME_COMPLETE)
                    return_to_main_page(wait)
                    save_progress(juror_id)
                    reset_search(wait)

            except Exception as e:
                log.error(f"Error on juror {juror_id}: {e}")
                write_outcome(EXCEL_FILE, data["row"], OUTCOME_ERROR)
                reset_search(wait)
                continue

        completed = True

    finally:
        if completed:
            delete_progress()
        teardown_browser(driver, log) # ALWAYS RUN NO MATTER WHAT

    if completed:
        prompt_and_combine(folders["screenshots"], EXCEL_FILE, log)

if __name__ == "__main__":
    main()