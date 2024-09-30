from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.utils import ImageReader
import mysql.connector
import matplotlib.pyplot as plt
from PIL import Image as PILImage
from io import BytesIO
from datetime import datetime
import database as db
# MySQL database connection


# Function to fetch industry and balance data
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

# Function to generate a pie chart for balance dues
def generate_pie_chart(balance_dues):
    budget_heads = [item['budget_head_name'] for item in balance_dues]
    balances = [item['balance'] for item in balance_dues]
    
    fig, ax = plt.subplots()
    ax.pie(balances, labels=budget_heads, autopct='%1.1f%%', colors=plt.cm.Paired.colors, startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    # Save the pie chart to a byte buffer
    buf = BytesIO()
    plt.savefig(buf, format='PNG')
    buf.seek(0)
    
    # Return pie chart as an Image object for ReportLab
    return buf

# Function to generate the PDF
def generate_invoice_pdf(industry_id):
    # Fetch data from database
    industry_details, balance_dues = fetch_data(industry_id)
    
    # Create PDF document
    pdf_file = f"invoice_{industry_details[0]}.pdf"

    doc = SimpleDocTemplate(pdf_file, pagesize=A4)
    elements = []

    # Define paragraph styles
    style_left = ParagraphStyle(
        name='LeftAlign',
        fontSize=12,
        spaceAfter=12
    )

    style_right = ParagraphStyle(
        name='RightAlign',
        fontSize=10,
        alignment=TA_RIGHT  # Align right for the date
    )

    
    # Add company logo (replace 'company_logo.png' with your image path)
    logo_image = r'D:\Python\KPEZDMC\images\comlogo.png'
    img = PILImage.open(logo_image)
    #img = img.resize((80, 80), PILImage.ANTIALIAS)
    logo_buffer = BytesIO()
    img.save(logo_buffer, format='PNG')
    logo_buffer.seek(0)
    
    logo = Image(logo_buffer, width=80, height=80)
    logo.hAlign = 'LEFT'
    elements.append(logo)
    
    # Add industry name, owner name, and date
    styles = getSampleStyleSheet()
    header = f"<font size=12>Industry: {industry_details[0]}<br/> Owner: {industry_details[1]}<br/></font><br/><br/><font size=10 align=right>Date: {datetime.now().strftime('%d-%m-%Y')}</font>"
    
    elements.append(Paragraph(header))
    
    # Add subject line
    subject = "<br/><br/><font size=12><b>Subject:</b> Request to Submit Outstanding Dues</font>"
    elements.append(Paragraph(subject))
    
    # Add greeting and request paragraph
    greeting = """
    <br/><br/>
    Dear Sir/Madam,<br/><br/>
    This is a polite reminder that you have outstanding dues under various budget heads. We kindly request you to submit the payments as soon as possible.<br/><br/>
    """
    elements.append(Paragraph(greeting, styles['Normal']))
    
    # Add balance dues table
    data = [['Budget Head', 'Amount Due']]  # Table header
    total_due = 0
    for due in balance_dues:
        data.append([due['budget_head_name'], f"${due['balance']:.2f}"])
        total_due += due['balance']
    
    data.append(['<b>Total</b>', f"${total_due:.2f}"])
    
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table)
    
    # Generate and add pie chart
    pie_chart = generate_pie_chart(balance_dues)
    pie_image = Image(pie_chart, width=200, height=200)
    elements.append(pie_image)
    
    # Add closing message and bank details
    closing = """
    <br/><br/>Please submit the balance dues at the earliest to the following account:<br/>
    <b>Bank Name:</b> XYZ Bank<br/>
    <b>Account Number:</b> 123456789<br/>
    <b>IFSC Code:</b> XYZ0001234<br/><br/>
    Thank you for your prompt action.<br/><br/>
    Sincerely,<br/>
    Accounts Department
    """
    elements.append(Paragraph(closing))
    
    # Build the PDF document
    doc.build(elements)
    print(f"Invoice PDF generated: {pdf_file}")

# Example usage:
industry_id = 100  # Replace with the actual industry ID
generate_invoice_pdf(industry_id)
