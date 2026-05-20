# Venire Automation 3.0

Automates juror record lookup for the State Attorney's Office — reducing a 65-hour manual process to a single unattended workday.

Developed for the **10th Judicial Circuit of Florida**. Follows NASA Power of 10 coding standards adapted for Python.

---

## What Problem It Solves

The State Attorney's Office receives venire lists with thousands of jurors that must each be looked up in a legal case database (CCIS), with results logged back to Excel. A previous automation (v2) handled this using image recognition and simulated mouse clicks — taking screenshots of the screen, locating UI elements by pixel matching, and using fixed sleep timers to wait for pages to load. It worked, but it was fragile and slow: 43 seconds per juror, meaning a 5,500-row venire took over 65 hours.

v3 replaces image recognition with direct Selenium browser automation and explicit element waits — cutting that to 4 seconds per juror and roughly 5 hours for the same run. It runs fully unattended.

---

## How It Works

1. Reads thousands of juror records from an Excel sheet (ID, name, date of birth)
2. Launches Chrome, logs into CCIS, and searches each juror by name and DOB
3. If a record is found, captures a PDF of the case summary page silently via Chrome DevTools Protocol
4. Writes the outcome back to Excel for every juror — found, not found, or error
5. On completion, optionally merges all PDFs and the Excel report into one combined file

If the program crashes mid-run, it picks up from the last completed juror automatically via `progress.txt`.

---

## Tech Stack

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.12 | Core language |
| Selenium | 4.x | Browser automation |
| webdriver-manager | latest | Auto-manages ChromeDriver version matching |
| openpyxl | 3.1.5 | Excel read/write |
| Chrome DevTools Protocol | — | Silent PDF generation |
| reportlab | latest | Excel-to-PDF conversion |
| pypdf | latest | PDF merging |
| logging | stdlib | Structured run logs |

---

## Results

| Metric | v2 (Image Recognition) | v3 (Selenium) |
|--------|------------------------|---------------|
| Time per juror | 43 seconds | ~4 seconds |
| Time for 5,500 jurors | ~65 hours | ~5 hours |
| Staff required during run | 1 (monitoring required) | 0 (fully unattended) |
| Crash recovery | Manual restart from beginning | Auto-resumes from last completed row |
| Audit trail | Inconsistent | Every row logged automatically |

---

## Project Structure

```
venire_3.0/
├── main.py              # Orchestration loop — setup, resume logic, main loop, teardown
├── browser.py           # All Selenium interactions with CCIS (login, search, PDF)
├── excel_handler.py     # Excel read/write using openpyxl
├── file_handler.py      # Folder creation, progress tracking, PDF path building
├── logger.py            # Structured logger — file + console handlers, duplicate guard
├── report_builder.py    # PDF merging and Excel-to-PDF conversion via reportlab/pypdf
├── cli.py               # argparse CLI interface for runtime flags
├── config.py            # Dataclass schemas and load_config() entry point
├── config.json          # All tunable constants — element IDs, timeouts, outcome strings
├── key.py               # Credentials — not committed to version control
├── VENIRE.xlsx          # Input Excel sheet — not committed to version control
└── screenshots/
    └── YYYY-MM-DD/
        ├── 1042_Smith_John.pdf
        └── YYYY-MM-DD.log
```

---

## Setup

1. Clone the repository
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate       # Windows
   source venv/bin/activate    # Mac/Linux
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create `key.py` in the project root with your credentials:
   ```python
   WEBSITE  = "https://flccis.com"
   USERNAME = "your_username"
   PASSWORD = "your_password"
   ```
5. Place `VENIRE.xlsx` in the project root. Required column layout:

   | Column A | Column B | Column C |
   |----------|----------|----------|
   | Juror ID | DOB | Name (Last, First Middle) |

6. Run:
   ```bash
   python main.py
   ```

---

## CLI Flags

All flags are optional. Running `python main.py` with no flags is a normal production run.

| Flag | Description |
|------|-------------|
| `--headless` | Run Chrome without a visible browser window |
| `--limit N` | Stop after processing N jurors (use for testing) |
| `--fresh` | Ignore `progress.txt` and restart from the beginning |
| `--combine` | Automatically combine all PDFs + Excel into one file when done |
| `--no-combine` | Skip the combine step entirely |

**Examples:**
```bash
python main.py --headless
python main.py --limit 10
python main.py --fresh --headless
python main.py --combine
```

---

## Configuration

All tunable values live in `config.json` — no need to touch source code for routine changes.

**Key sections:**

- `Browser.Login` — element IDs for the login form
- `Browser.Search` — element IDs and XPaths for the search form
- `Browser.Results` — element ID for the view selection button
- `Browser.Navigation` — element IDs for back buttons and reset button
- `Browser.Seconds` — timeout values for WebDriverWait and sleep pauses
- `App` — outcome label strings written to Excel, Excel filename

---

## Outcomes Written to Excel (Column D)

| Value | Meaning |
|-------|---------|
| `CH Found` | A record was found; PDF saved |
| *(blank)* | No match returned by CCIS |
| `Error — check manually` | An unexpected exception occurred on this row |
| `Warning — bad format` | Row could not be parsed (missing name, DOB, or bad format) |

The exact strings are configurable in `config.json` under `App`.

---

## Logging

Every run produces a `.log` file inside the dated screenshot folder:

```
screenshots/
└── 2026-05-05/
    ├── 1042_Smith_John.pdf
    ├── 1043_Doe_Jane.pdf
    └── 2026-05-05.log
```

**Log format:**
```
2026-05-05 10:32:11 - Venire - INFO  - Browser started successfully
2026-05-05 10:32:14 - Venire - INFO  - 1/5500
2026-05-05 10:32:18 - Venire - INFO  - 2/5500
2026-05-05 10:33:02 - Venire - ERROR - Error on juror 1047: TimeoutException
```

---

## Crash Recovery

When a run is interrupted, `progress.txt` (inside `results/`) stores the last successfully completed juror ID. On the next run, the script reads this file and skips forward to resume where it left off.

To force a clean restart instead, pass `--fresh`.

---

## Coding Standards

Follows **NASA Power of 10** principles adapted for Python:

- Single-responsibility functions — each function does exactly one thing
- Explicit type hints on every function signature
- Docstrings on every function with `Args`, `Returns`, and `Example`
- Named constants — no magic numbers or hardcoded strings in logic
- No silent failures — all exceptions caught, logged, and written to Excel
- No globals — all dependencies passed explicitly as parameters

---

## Author

Nick Pham — IT Automation Developer, 10th Judicial Circuit of Florida