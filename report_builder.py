# Report Builder

# STANDARD LIBRARY IMPORTS
import os
from pathlib import Path

import openpyxl
# THIRD-PARTY IMPORTS
from openpyxl import load_workbook
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from pypdf import PdfWriter, PdfReader

def excel_to_pdf(excel_path: str, output_pdf_path: str) -> str:
    if not os.path.exists(excel_path): # If the file path does not exist is not there.
        raise FileNotFoundError(f"File not found: {excel_path}") # Raise an error if the Excel sheet cannot be found.
    workbook = load_workbook(excel_path)
    worksheet = workbook.active

    data = []
    for row in worksheet.iter_rows(values_only=True):
        data.append([str(cell) if cell is not None else "" for cell in row])

    document = SimpleDocTemplate(output_pdf_path, pagesize=letter)

    document.build([Table(data)])

    return output_pdf_path
