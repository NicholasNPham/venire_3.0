import argparse

def parse_args() -> argparse.Namespace:
    """
    Parses command-line arguments for the Venire Automation script.

    Returns:
        argparse.Namespace: Parsed arguments with the following attributes:
            - headless (bool): True if --headless flag is passed, False by default.
            - limit (int | None): Max jurors to process, None processes all rows.
            - combine (bool | None): True/False if --combine/--no-combine passed, None prompts user.
            - fresh (bool): True if --fresh flag is passed, False by default.

    Example:
        $ python main.py --headless --limit 50
        Namespace(headless=True, limit=50, combine=None, fresh=False)
    """
    parser = argparse.ArgumentParser(description='Automates juror record searches on flccis.com and saves results as PDFs.')

    # --headless: this will allow selenium to either run headless and the opposite.
    parser.add_argument("--headless", action="store_true", help="Run Chrome without a visible browser window.")
    # --limit: this will allow you to run a specific amount of juror_id rows and stops at that set limit.
    parser.add_argument("--limit", type=int, default=None, help="Limit the number of jurors processed. Omit to process all rows. [Testing use]")
    # --combine: this will automatically combine the Excel sheet turn pdf and all screenshots into one document.
    parser.add_argument("--combine", action=argparse.BooleanOptionalAction, default=None, help="Combine all jurors into one PDF including the Excel sheet.")
    # --fresh: this will remove the progress.txt file and restart the run from the start instead of last row ran.
    parser.add_argument("--fresh", action="store_true", help="Ignore the progress.txt file and start a fresh loop.")

    return parser.parse_args()