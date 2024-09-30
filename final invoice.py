from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
import matplotlib.pyplot as plt
import mysql.connector
from datetime import datetime
import database as db

# Function to fetch data from MySQL database
def fetch_data(industry_id):
    cursor, con = db.database_connect()
    cursor.execute("use kpezdmc_version1")
    # Query to get industry details
    cursor.execute("""
    select i.ind_name,o.ownname,p.plot_number,p.Area 
    from plots p 
    join 
    plot_ownership po 
    on 
    p.id = po.plot_id 
    join
    ownertable o 
    on o.id = po.owner_id 
    left join 
    industries i 
    on i.plot_id = p.id where i.id = %s
    """, (industry_id,))
    industry_details = cursor.fetchone()
    
    # Query to get balance dues
    cursor.execute("""
     select b.budget_head_name,bb.balance 
    from balance bb 
    join budget_heads b 
    on b.budget_head_id = bb.budget_head_id 
    where bb.industry_id = %s
        """, (industry_id,))
    balance_dues = cursor.fetchall()
    
    cursor.close()
    return industry_details, balance_dues

# Function to create a pie chart
def create_pie_chart(data):
    labels = [row[0] for row in data]  # Budget heads
    balances = [row[1] for row in data]  # Balances
    
    plt.figure(figsize=(2, 2))
    plt.pie(balances, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')  # Equal aspect ratio ensures pie is drawn as a circle.
    
    # Save the pie chart as an image
    plt.savefig('pie_chart.png', format='png', bbox_inches='tight', dpi=150)
    plt.close()

# Function to generate PDF invoice notification
def generate_pdf():
    data,bal_due = fetch_data(100)
    if not data:
        print("No data found.")
        return

    # Create the PDF
    pdf_filename = 'industry_invoice.pdf'
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    
    # Create a list for the PDF elements
    elements = []

    # Add company logo
    logo = Image('D:\Python\KPEZDMC\images\comlogo.png')
    logo.width = 3 * inch
    logo.height = 1.5 * inch
    elements.append(logo)

    # Prepare styles
    styles = getSampleStyleSheet()
    
    # Add Industry and Owner Name
    
    industry_name, owner_name = data[0], data[1]  # Unpacking first row (assuming single industry)
    print(industry_name)
    elements.append(Paragraph(f'<b>Industry Name:</b> {industry_name}', styles['Normal']))
    elements.append(Paragraph(f'<b>Owner Name:</b> {owner_name}', styles['Normal']))
    
    # Add Date
    date_string = f'Date: {datetime.now().strftime("%d-%m-%Y")}'
    elements.append(Paragraph(date_string, styles['Normal']))
    
    # Add Subject Line
    elements.append(Paragraph('<b>Subject:</b> Submission of Balance Dues', styles['Normal']))
    
    # Add Greeting and Request Paragraph
    greeting_message = 'Dear Sir/Madam,<br/><br/>We kindly request you to submit the balance dues as per the details below.'
    elements.append(Paragraph(greeting_message, styles['Normal']))
    
    # Prepare Balance Details Table
    balance_details = [['Budget Head', 'Balance (Amount)']]  # Header row
    total_balance = 0
    for row in bal_due:
        budget_head = row[0]
        balance = row[1]
        total_balance += balance
        balance_details.append([budget_head, f'${balance:,.2f}'])
    
    # Create Table for Balance Details
    table = Table(balance_details)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elements.append(table)

    # Insert Pie Chart Image
    create_pie_chart(bal_due)
    pie_chart_image = Image('pie_chart.png')
    pie_chart_image.width = 4 * inch
    pie_chart_image.height = 4 * inch
    elements.append(pie_chart_image)
    
    # Closing Message with Bank Details
    closing_message = (
        'We kindly request you to submit the balance dues at your earliest convenience. '
        'The payment can be made to the following account:<br/><br/>'
        'Account Name: Industry Payment Services<br/>'
        'Account Number: 123456789<br/>'
        'Bank: National Bank<br/>'
        'Branch Code: 00112233'
    )
    elements.append(Paragraph(closing_message, styles['Normal']))

    # Build the PDF
    doc.build(elements)
    print(f"PDF generated successfully: {pdf_filename}")

# Generate the PDF
generate_pdf()
