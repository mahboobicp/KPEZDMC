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

# Function to create a bar chart
def create_bar_chart(data):
    labels = [row[0] for row in data]  # Budget heads
    balances = [row[1] for row in data]  # Balances
    
    plt.figure(figsize=(2.5, 1))
    plt.bar(balances, labels, color='skyblue')
    plt.xlabel('Balance Amount',fontsize=5)
    plt.xticks(rotation=0,fontsize=4)
    plt.yticks(rotation=0,fontsize=4)
    
    # Save the bar chart as an image
    plt.tight_layout()
    plt.savefig('bar_chart.png', format='png', bbox_inches='tight', dpi=150)
    plt.close()

# Function to generate PDF invoice notification
def generate_pdf():
    data,bal_due = fetch_data(110)
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
    logo.width = 2.5 * inch
    logo.height = 1 * inch
    elements.append(logo)

    # Prepare styles
    styles = getSampleStyleSheet()
    styles['Normal'].fontSize = 12  # Set font size to 12
    right_aligned_style = styles['Normal'].clone('RightAligned')
    right_aligned_style.alignment = 2  # 0=left, 1=center, 2=right
    # Add Industry and Owner Name
    industry_name, owner_name,pltn,pltarea = data[0], data[1],data[2],data[3]  # Unpacking first row (assuming single industry)
    #elements.append(Paragraph(f'<b><br/>Industry :</b> {industry_name}', styles['Normal']))
    # Add industry Name and Date
    date_string = f'Date: {datetime.now().strftime("%d-%m-%Y")}'
    plotnum = f'Plot No. {pltn} Area : {pltarea}'
    print(plotnum)
    ######################################3
    # Prepare the table data
    data = [
        [Paragraph(f'Industry Name: {industry_name}', styles['Normal']), Paragraph(f'  {date_string}', styles['Normal'])],
        [Paragraph(f'Owner Name: {owner_name}', styles['Normal']), ''],  # Empty cell for alignment
        [Paragraph(f'{plotnum}', styles['Normal']), ''],
    ]

    # Create a Table
    header_table = Table(data, colWidths=[320, 150])  # Adjust widths as necessary
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 10), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),  # Align left for industry and owner
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),  # Align right for date
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('GRID', (0, 0), (-1, -1), 1, colors.white),
    ]))

    # Create the PDF elements list
    #elements.append("<br/>")
    elements.append(header_table)
    #########################################################
    
    
    # Add Subject Line
    elements.append(Paragraph('<b><br/>SUBJECT:    </b> NOTICE FOR PAYMNET OF OUTSTANDING ZONE DUES', styles['Normal']))
    elements.append(Paragraph('<br/><br/>', styles['Normal']))  # Add space after subject line

    # Add Greeting and Request Paragraph
    greeting_message = 'Dear Sir/Madam,<br/><br/>The under mentioned amount/charges are Outstanding dues aganist your unit as per the following break up.<br/><br/>'
    elements.append(Paragraph(greeting_message, styles['Normal']))
    elements.append(Paragraph('<br/>', styles['Normal']))  # Add space before the table

    # Prepare Balance Details Table
    zonebalance_details = [['Zone Budget Head', 'Balance (Amount)']]  # Header row
    zfcbalance_details = [['ZFC Budget Head', 'Balance (Amount)']]  # Header row
    totalzone = 0
    totalzfc = 0
    for row in bal_due:
        budget_head = row[0]
        balance = float(row[1])
        if row[0] =='Maintenance' or budget_head =="ZFC Maintenance":
            totalzone=totalzone+balance
            print(budget_head)
            zonebalance_details.append([budget_head, f'{balance:,.2f}'])
        elif budget_head is "ZFC Surcharge" or budget_head is "ZFC Maintenance":
            totalzfc += balance
            zfcbalance_details.append([budget_head, f'{balance:,.2f}'])
            print(budget_head)
    zonebalance_details.append(['Grand Total',totalzone])  
    print(f"ZMC : {totalzfc} and Zone : {totalzone}")
    # Create Table for Balance Details
    zonetable = Table(zonebalance_details,colWidths=[110, 90])
    zonetable.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elements.append(zonetable)
    # End of Zone Table 
    #Start of ZFC Table 
      # Create Table for Balance Details
    zfctable = Table(zfcbalance_details,colWidths=[110, 90])
    zfctable.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elements.append(zfctable)

    """ # Insert Bar Chart Image
    create_bar_chart(bal_due)
    bar_chart_image = Image('bar_chart.png')
    bar_chart_image.width = 2 * inch
    bar_chart_image.height = 1 * inch
    elements.append(bar_chart_image) """

    # Closing Message with Bank Details
    closing_message = (
        '<br/>We kindly request you to submit the balance dues at your earliest convenience. '
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
