# Venire Automation 3.0

Automates juror record lookup for the State Attorney's Office — reducing a 65-hour process to a single unattended workday.

Developed for the **10th Judicial Circuit of Florida**. Follows NASA Power of 10 coding standards adapted for Python.

---

## What Problem It Solves

The State Attorney's Office receives venire lists with thousands of jurors that must each be looked up in a legal case database (CCIS), with results logged back to Excel. A previous automation (v2) handled this using image recognition and simulated mouse clicks — taking screenshots of the screen, locating UI elements by pixel matching, and using fixed sleep timers to wait for pages to load. It worked, but it was fragile and slow: 43 seconds per juror, meaning a 5,500-row venire took over 65 hours.

v3 replaces image recognition with direct Selenium browser automation and explicit element waits — cutting that to 4 seconds per juror and 5 hours for the same run.

---

## How It Works

1. Reads thousands of juror records from an Excel sheet (ID, name, date of birth)
2. Launches a browser, logs into CCIS, and searches each juror by name and DOB
3. If a record is found, captures a PDF of the case summary page silently via Chrome DevTools Protocol
4. Writes the outcome back to Excel for every juror — found, not found, or error
5. On completion, optionally merges all PDFs and the Excel report into one combined file

If the program crashes mid-run, it picks up from the last completed juror automatically.

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.12 | Core language |
| Selenium 4 | Browser automation |
| webdriver-manager | Auto-manages ChromeDriver version matching |
| openpyxl | Excel read/write |
| Chrome DevTools Protocol | Silent PDF generation |
| reportlab | Excel-to-PDF conversion |
| pypdf | PDF merging |
| logging | Structured run logs |

---

## Results

| Metric | v2 (Image Recognition) | v3 (Selenium) |
|--------|------------------------|---------------|
| Time per juror | 43 seconds | 4 seconds |
| Time for 5,500 jurors | ~65 hours | ~5 hours |
| Staff required during run | 1 (monitoring required) | 0 (fully unattended) |
| Crash recovery | Manual restart from beginning | Auto-resumes from last completed row |
| Audit trail | Inconsistent | Every row logged automatically |

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
├── config.py          # Dataclass schemas and load_config() entry point
├── config.json        # All tunable constants — element IDs, timeouts, outcome strings
├── key.py             # Credentials (not committed to version control)
├── VENIRE.xlsx        # Input Excel sheet (not committed to version control)
└── results/           # Run artifacts — dated subfolders with PDFs and log files
```

---

## Coding Standards

Follows **NASA Power of 10** principles adapted for Python:

- Single-responsibility functions
- Explicit type hints on every function signature
- Docstrings on every function with `Args`, `Returns`, and `Examples`
- Named constants — no magic numbers or hardcoded strings
- No silent failures — all exceptions caught, logged, and written to Excel
- No globals — all dependencies passed explicitly as parameters

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
   WEBSITE  = "https://flccis.com"
   USERNAME = "your_username"
   PASSWORD = "your_password"
   ```
5. Place `VENIRE.xlsx` in the project root with columns: `Juror ID | DOB | Name`
6. Run:
   ```bash
   python main.py
   ```

---

## Logging

Every run produces a `.log` file inside the dated output folder:

```
screenshots/
└── 2026-05-05/
    ├── 1042_Smith_John.pdf
    ├── 1043_Doe_Jane.pdf
    └── 2026-05-05.log
```

```
2026-05-05 10:32:11 - Venire - INFO - Browser started successfully
2026-05-05 10:32:14 - Venire - INFO - 1/5500
2026-05-05 10:32:18 - Venire - INFO - 2/5500
2026-05-05 10:33:02 - Venire - ERROR - Error on juror 1047: TimeoutException
```

---

## Roadmap

| Tier | Feature | Status |
|------|---------|--------|
| 1 | Structured logging | ✅ Complete |
| 2 | Externalized config file (JSON) | ✅ Complete |
| 3 | Auto-managed ChromeDriver via webdriver-manager | 🔜 Next |
| 4 | CLI interface with `argparse` | Planned |
| 5 | REST API wrapper (FastAPI) | Planned |
| 6 | LLM integration for result summarization | Planned |

---

## Author

Nick Pham — IT Automation Developer