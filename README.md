# Venire Automation 3.0

A production-grade Python automation tool that scrapes juror records from a legal case information system (CCIS), processes thousands of rows from an Excel sheet, generates PDFs of results, and logs outcomes back to Excel — completing a full run in a single workday.

Developed for the **State Attorney's Office — 10th Judicial Circuit of Florida**. Follows NASA Power of 10 coding standards adapted for Python.

---

## Features

- Selenium-based web scraping with explicit waits — no brittle `time.sleep()` calls
- Processes thousands of juror records from Excel (ID, DOB, name) in a single run
- Generates PDFs of case summary pages via Chrome DevTools Protocol
- Writes outcomes back to Excel (`CH Found`, `No matches found`, `Error - check manually`)
- Crash recovery via `progress.txt` — resumes from last completed juror on restart
- Structured logging to both console and dated log file — no silent failures
- Optional end-of-run report: merges all juror PDFs and Excel data into one combined PDF

---

## Project Structure

```
venire_3.0/
├── main.py            # Orchestration loop — setup, resume logic, main loop, teardown
├── browser.py         # Selenium interactions with CCIS (login, search, PDF generation)
├── excel_handler.py   # Excel read/write operations using openpyxl
├── file_handler.py    # Folder creation, progress tracking, PDF path building
├── logger.py          # Structured logger — file + console handlers, duplicate guard
├── report_builder.py  # PDF merging and Excel-to-PDF conversion
├── key.py             # Credentials and paths (not committed to version control)
├── VENIRE.xlsx        # Input Excel sheet (not committed to version control)
└── results/           # Run artifacts — dated subfolders with PDFs and log files
```

---

## Coding Standards

This project follows **NASA Power of 10** principles adapted for Python:

- Single-responsibility functions
- Explicit type hints on every function signature
- Docstrings on every function with `Args`, `Returns`, and `Examples`
- Named constants — no magic numbers or hardcoded strings
- No silent failures — all exceptions are caught, logged, and written to Excel
- No globals — dependencies (logger, driver, wait) passed explicitly as parameters

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.12 | Core language |
| Selenium 4 | Browser automation |
| openpyxl | Excel read/write |
| Chrome DevTools Protocol | Silent PDF generation |
| reportlab | Excel-to-PDF conversion |
| pypdf | PDF merging |
| logging | Structured run logs |

---

## How It Works

1. **Setup** — Creates dated output folders, initializes the logger, loads jurors from Excel, launches browser and logs in
2. **Default outcomes** — Writes `Error - check manually` to every row before the loop starts, so any crash leaves an auditable trail
3. **Resume logic** — Checks for `progress.txt`; if found, skips ahead to the last completed juror
4. **Main loop** — For each juror: inputs search criteria, checks for results, generates and saves PDF if found, writes outcome to Excel, saves progress
5. **Teardown** — Deletes progress file on clean finish, always closes the browser via `finally` block
6. **Report** — Optionally merges all PDFs and Excel data into a single combined report

---

## Logging

Every run produces a `.log` file inside the dated output folder alongside the PDFs:

```
screenshots/
└── 2026-05-05/
    ├── 1042_Smith_John.pdf
    ├── 1043_Doe_Jane.pdf
    └── 2026-05-05.log
```

Log format:
```
2026-05-05 10:32:11 - Venire - INFO - Browser started successfully
2026-05-05 10:32:14 - Venire - INFO - 1/2000
2026-05-05 10:32:15 - Venire - INFO - 2/2000
2026-05-05 10:33:02 - Venire - ERROR - Error on juror 1047: TimeoutException
```

---

## Setup

1. Clone the repository
2. Create and activate a virtual environment
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```
3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
4. Create `key.py` with your credentials:
   ```python
   WEBSITE   = "https://flccis.com"
   CHROME_PATH = r"path\to\chromedriver.exe"
   USERNAME  = "your_username"
   PASSWORD  = "your_password"
   ```
5. Place `VENIRE.xlsx` in the project root with columns: `Juror ID | DOB | Name`
6. Run:
   ```bash
   python main.py
   ```

---

## Roadmap

| Tier | Feature | Status |
|------|---------|--------|
| 1 | Structured logging | ✅ Complete |
| 2 | Externalized config file (JSON) | 🔜 Next |
| 3 | CLI interface with `argparse` | Planned |
| 4 | REST API wrapper (FastAPI) | Planned |
| 5 | LLM integration for result summarization | Planned |

---

## Author

Nick Pham — IT Automation Developer