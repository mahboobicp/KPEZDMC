from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

# Create a PDF document
pdf = SimpleDocTemplate("table_with_empty_row.pdf", pagesize=A4)

# Sample data for the table
data = [
    ["Header 1", "Header 2"],
    ["Row 1 Col 1", "Row 1 Col 2"],
    ["Row 2 Col 1", "Row 2 Col 2"],
    [],  # This is the empty row
    ["Row 3 Col 1", "Row 3 Col 2"],
]

# Create a table with the data
table = Table(data)

# Define a table style
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Header background color
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header text color
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align all cells
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Padding for header
    ('TOPPADDING', (0, 0), (-1, 0), 12),  # Padding for header
    ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Grid lines
]))

# Build the PDF with the table
pdf.build([table])

print("PDF created successfully.")
