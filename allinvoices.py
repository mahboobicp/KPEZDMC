from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import matplotlib.pyplot as plt
import mysql.connector
from datetime import datetime
import database as db
from reportlab.lib.pagesizes import A4, letter
def add_footer(canvas, doc):
    # Path to the image file
    image_path = r"D:\Python\KPEZDMC\images\footer.png"
    
    # Position the image at the bottom left (adjust values for positioning)
    image_width = 7 * inch  # Image width (in inches)
    image_height = 0.5 * inch  # Image height (in inches)
    
    # X and Y positions for the image
    x_position = 0.5 * inch  # Left margin
    y_position = 0.5 * inch  # Footer height from bottom of the page
    
    # Draw the image on the canvas
    canvas.drawImage(image_path, x_position, y_position, width=image_width, height=image_height)

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
    where bb.industry_id = %s and bb.balance <> 0
        """, (industry_id,))
    balance_dues = cursor.fetchall()


    cursor.close()
    return industry_details, balance_dues


# Function to generate PDF invoice notification
def generate_pdf(indid):
    global doc
    data,bal_due = fetch_data(indid)
    if not data:
        print("No data found.")
        return

    # Create the PDF
    pdf_filename = 'all_industries_invoice.pdf'
    doc = SimpleDocTemplate(pdf_filename, pagesize=A4)
    left_margin = 1 * inch
    top_margin = 0 * inch
    right_margin = 1 * inch
    bottom_margin = 1 * inch
    doc.topMargin = top_margin
    doc.leftMargin = left_margin
    doc.rightMargin = right_margin
    # Create a list for the PDF elements
    elements = []

    # Add company logo
    logo = Image('D:\Python\KPEZDMC\images\comlogo.png')
    logo.width = 1 * inch
    logo.height = 1 * inch
    elements.append(logo)

    # Prepare styles
    styles = getSampleStyleSheet()
    styles['Normal'].fontSize = 12  # Set font size to 12
    right_aligned_style = styles['Normal'].clone('RightAligned')
    right_aligned_style.alignment = 2  # 0=left, 1=center, 2=right
    # Define a custom paragraph style
    custom_style = ParagraphStyle(
    name="CustomStyle",
    fontName="Helvetica",  # Change the font (e.g., Helvetica, Times-Roman, Courier)
    fontSize=12,  # Font size
    leading=16,  # Line spacing (leading is space between lines)
    spaceAfter=12,  # Space after the paragraph
    )
    right_aligned_style = ParagraphStyle(
    name='RightAligned',
    fontSize=12,
    alignment=2,  # 0: LEFT, 1: CENTER, 2: RIGHT
    )
    # Add Industry and Owner Name
    industry_name, owner_name,pltn,pltarea = data[0], data[1],data[2],data[3]  # Unpacking first row (assuming single industry)
    #elements.append(Paragraph(f'<b><br/>Industry :</b> {industry_name}', styles['Normal']))
    # Add industry Name and Date
    date_string = f'Date: {datetime.now().strftime("%d-%m-%Y")}'
    plotnum = f'<b>Plot No :</b> {pltn} Area : {pltarea}'
    print(plotnum)
    ######################################3
    # Prepare the table data
    data = [
        [Paragraph(f'<b>No. (IEM/NSR) ________</b>', styles['Normal']), Paragraph(f'  {date_string}', styles['Normal'])],
        [],
        [Paragraph(f'<b>Industry Name:</b> {industry_name}', styles['Normal']), ''],
        [Paragraph(f'<b>Owner Name:</b> {owner_name}', styles['Normal']), ''],  # Empty cell for alignment
        [Paragraph(f'{plotnum}', styles['Normal']), ''],
    ]

    # Create a Table
    header_table = Table(data, colWidths=[300, 150])  # Adjust widths as necessary
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 10), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),  # Align left for industry and owner
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),  # Align right for date
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('GRID', (0, 0), (-1, -1), 1, colors.white),
          # Control cell padding for all cells (LEFT, RIGHT, TOP, BOTTOM)
       ('PADDING', (0, 1), (-1, -1), 1),  # Decrease cell padding for rows
       ('BOTTOMPADDING', (0, 1), (-1, -1), 2),  # Decrease bottom padding for rows
       ('TOPPADDING', (0, 1), (-1, -1), 2),  # Decrease top padding for rows

        # Control space before and after the table (to other eleme                  # Space after the table
    ]))

    # Create the PDF elements list
    #elements.append("<br/>")
    elements.append(header_table)
    #########################################################
    
    
    # Add Subject Line
    elements.append(Paragraph('<b><br/>SUBJECT:    </b> NOTICE FOR PAYMNET OF OUTSTANDING ZONE DUES', styles['Normal']))
    elements.append(Paragraph('<br/><br/>', styles['Normal']))  # Add space after subject line

    # Add Greeting and Request Paragraph
    greeting_message = 'Dear Sir/Madam,<br/><br/>The under mentioned amount/charges are Outstanding dues aganist your unit as per the following break up.<br/>'
    elements.append(Paragraph(greeting_message, custom_style))
    elements.append(Paragraph('<br/>', styles['Normal']))  # Add space before the table
    
    # Prepare Balance Details Table
    zonebalance_details = [['Zone Budget Head', 'Balance (Amount)']]  # Header row
    zfcbalance_details = [['ZFC Budget Head', 'Balance (Amount)']]  # Header row
    totalzone = 0
    totalzfc = 0
    for row in bal_due:
        budget_head = row[0]
        balance = float(row[1])
        if ((row[0] !='ZFC Surcharge') and (row[0] !='ZFC Maintenance')):
            totalzone=totalzone+balance
            print(budget_head)
            zonebalance_details.append([budget_head, f'{balance:,.2f}'])
        else:   
            totalzfc =totalzfc + balance
            zfcbalance_details.append([budget_head, f'{balance:,.2f}'])
            print(budget_head)
    zonebalance_details.append(['Grand Total',totalzone])
    zfcbalance_details.append(['Grand Total', totalzfc])  
    print(f"ZFC : {totalzfc} and Zone : {totalzone}")
    # Create Table for Balance Details
    zonetable = Table(zonebalance_details,colWidths=[120, 100])
    zonetable.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    #elements.append(zonetable)
    # End of Zone Table 
    #Start of ZFC Table 
      # Create Table for Balance Details
    zfctable = Table(zfcbalance_details,colWidths=[120, 100])
    zfctable.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    #elements.append(zfctable)
    paragraph = Paragraph(
    "<font size='8'><b>Bank : The Bank of Khyber (BOK)</b><br/></font>"
    "<font size='8'><b>AC No :</b> 2008826668<br/></font>"
    "<font size='8'><b> Title :</b>Khyber Pakhtunkhwa Economic Zone Development and Managment Company-Non Checking</font><br/> "
    "<font size='8'><b> Branch :</b>Nowshera Economic Zone Branch (0320)</font><br/>"
    "<font size='8'><b>Submit Zone Dues in Above Title!</b></font><br/><br/><br/>",
    styles['Normal']
    )
    paragraph2 = Paragraph(
    "<font size='8'><b>Bank : The Bank of Khyber (BOK)</b><br/></font>"
    "<font size='8'><b>AC No :</b> 2007908795<br/></font>"
    "<font size='8'><b> Title :</b>Zone Facilitation Committee NEZ</font><br/> "
    "<font size='8'><b> Branch :</b>Nowshera Economic Zone Branch (0320)</font><br/>"
    "<font size='8'><b>Submit ZFC Dues in Above Title!</b></font><br/><br/>",
    styles['Normal']
    )
    # Main Table
    main_table_data = [
        [[zonetable,zfctable], [paragraph,paragraph2]],  # First row with sub-tables in left column and paragraph in right column
    ]
    
    # Define the main table and its style
    main_table = Table(main_table_data, colWidths=[3.5 * inch, 2.5 * inch])  # Adjust column widths to fit page layout

    main_table.setStyle(TableStyle([
    ('GRID', (0, 0), (-1, -1), 1, colors.white),
    ('ALIGN', (0, 0), (0, 0), 'CENTER'),  # Center the left column (containing sub-tables)
    ('ALIGN', (1, 0), (1, 0), 'CENTER'),  # Center the right column (containing paragraph)
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Center vertically within the row
    ]))
    elements.append(main_table)
    """ # Insert Bar Chart Image
    create_bar_chart(bal_due)
    bar_chart_image = Image('bar_chart.png')
    bar_chart_image.width = 2 * inch
    bar_chart_image.height = 1 * inch
    elements.append(bar_chart_image) """

    # Closing Message with Bank Details
    closing_message = (
        '<br/><b>You are advised to deposit :</b><br/>'
        'KPEZDMC Charges in the Bank of Khyber, Nowshera Economic Zone Branch (0320) in Account # 2008826668 Titled : Khyber Pakhtunkhwa Economic Zone Development and Managment Company-Non Checking<br/>'
        '<b>whereas</b><br/>'
        'Zone Facilitation Committee (ZFC) charges in the bank of Khyber, Nowshera Economic Zone Branch (0320) in Account # 2007908795 Titled : Zone Facilitation Committee NEZ, at your earliest'
        '<br/><br/>'
        'KPEZDMC aims to develop and manage world class industerial estates to help organize and establish planned and rapid industrialization in Khyber Pakhtunkhwa'
        '<br/><br/> Thanking you in anticiption.'
    )
    elements.append(Paragraph(closing_message,custom_style))
    elements.append(Paragraph('Accounts Officer NEZ',right_aligned_style))
    # Build the PDF
    return elements
    print(f"PDF generated successfully: {pdf_filename}")

# code to call all industries

def main_code():
    global doc,elements
    flowables =[]
    cursor, con = db.database_connect()
    cursor.execute("use kpezdmc_version1")
    cursor.execute("select id from industries;")
    industry_details = cursor.fetchall()
    flowables = []

    # Simulate calling the page content generator function multiple times
    for i in industry_details:  # Example: Generate 3 pages
        print(i[0])
        page_content = generate_pdf(i[0])
        flowables.extend(page_content)  # Add the generated page content
    
    # Build the PDF with the list of flowables (pages and page breaks)
    doc.build(flowables,onFirstPage=add_footer, onLaterPages=add_footer)

