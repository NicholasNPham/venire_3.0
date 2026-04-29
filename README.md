# Venire Automation
 
Automates juror background lookups in CCIS by reading a juror Excel sheet, searching each juror by name and date of birth, generating a PDF of their case summary page, and writing the outcome back to the Excel file.
 
---
 
## Project Structure
 
```
venire_3.0/
│
├── main.py            # Entry point — runs the full batch loop
├── browser.py         # Selenium automation — all CCIS interactions
├── excel_handler.py   # Reads juror data and writes outcomes to Excel
├── file_handler.py    # Folder creation, PDF paths, progress tracking
├── key.py             # Credentials and config (not committed to version control)
│
├── screenshots/
│   └── YYYY-MM-DD/    # PDFs saved here, one folder per run date
│
└── results/
    └── progress.txt   # Resume file — created during run, deleted on completion
```
 
---
 
## Requirements
 
- Python 3.10+
- Google Chrome (installed)
- ChromeDriver (matching your Chrome version)
- Dependencies:
```bash
pip install selenium openpyxl
```
 
---
 
## Setup
 
1. Clone or copy the project folder to your machine.
2. Create a `key.py` file in the project root with the following:
```python
WEBSITE        = "https://your-ccis-url.com"
CHROME_PATH    = r"C:\path\to\chromedriver.exe"
USERNAME       = "your_username"
PASSWORD       = "your_password"
 
# Used for browser.py test runs only
TEST_FIRST_NAME    = "John"
TEST_LAST_NAME     = "Smith"
TEST_DATE_OF_BIRTH = "04/23/1985"
```
 
3. Place your juror Excel file in the project root. The file must be named:
```
TEST VENIRE EXCEL.xlsx
```
 
4. The Excel file must have the following column layout in `Sheet1`:
| Column A  | Column B       | Column C       | Column D  |
|-----------|----------------|----------------|-----------|
| Juror ID  | Date of Birth  | Name           | Outcome   |
 
Names must be formatted as `Last, First Middle` (e.g., `Smith, John Michael`).
 
---
 
## Running
 
```bash
python main.py
```
 
The script will:
1. Create `screenshots/YYYY-MM-DD/` and `results/` folders if they don't exist
2. Load all jurors from the Excel file
3. Stamp every row with `Error - check manually` as a safety default
4. Open Chrome and log into CCIS
5. Search each juror, generate a PDF if found, and write the outcome to Excel
6. Save progress after each completed row
7. Delete the progress file and close the browser when finished
---
 
## Outcomes Written to Excel
 
| Outcome | Meaning |
|---|---|
| `CH Found` | Juror was found in CCIS and PDF was saved |
| `No matches found` | CCIS returned no results for this juror |
| `Error - check manually` | Unexpected error during processing — check manually |
| `Warning - Could not confirm...` | Name could not be parsed from Excel — check formatting |
 
---
 
## Resume After Crash
 
If the script stops mid-batch, a `results/progress.txt` file will contain the last successfully completed juror ID. On the next run, the script will automatically resume from where it left off.
 
To force a fresh run from the top, delete `results/progress.txt` before running.
 
---
 
## Output
 
PDFs are saved to:
```
screenshots/YYYY-MM-DD/JurorID_LastName_FirstName.pdf
```
 
Example:
```
screenshots/2025-04-29/1042_Smith_John.pdf
```
 
---
 
## Notes
 
- `key.py` contains credentials and must never be committed to version control. Add it to `.gitignore`.
- The script processes roughly one juror every 4 seconds. A full 4,500-row batch takes approximately 5 hours.
- Names formatted as `LAST1 LAST2, FIRST` (double last names) will be flagged with a warning outcome and skipped — check those manually.
---
 
## Author
 
Nicholas Pham
