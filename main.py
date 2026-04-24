# STANDARD LIBRARY IMPORTS

# LOCAL IMPORTS
from excel_handler import load_jurors

# THIRD-PARTY LIBRARY IMPORTS

# CONSTANTS

# FUNCTIONS

# MAIN LOOP SETUP
jurors = load_jurors("TEST VENIRE EXCEL.xlsx")

# MAIN LOOP
print(jurors)
