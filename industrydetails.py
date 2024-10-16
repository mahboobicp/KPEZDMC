import mysql.connector
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.platypus import Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import altair as alt
import pandas as pd
from reportlab.pdfgen import canvas
import database as db
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF
from reportlab.graphics.charts.barcharts import VerticalBarChart
from io import BytesIO
from reportlab.lib.units import inch

def add_header_footer(canvas, doc):
    header_image_path = r"D:\Python\KPEZDMC\images\comlogo.png"
    footer_image_path = r"D:\Python\KPEZDMC\images\footer.png"
    width, height = A4
    
    # Add header image
    canvas.drawImage(header_image_path, x=20, y=height - 60, width=550, height=50)  # Adjust positioning
    
    # Add footer image
    canvas.drawImage(footer_image_path, x=32, y=30, width=500, height=50)  # Adjust positioning

    # Add page number in footer (optional)
    canvas.setFont("Helvetica", 10)
    page_num_text = f"Page {doc.page}"
    canvas.drawRightString(width - 30, 40, page_num_text)
# Connect to the MySQL database



def industrydata(indid):
    cursor,con = db.database_connect()

    # Query to fetch industry details, owner details, and plot details
    industry_query = f"SELECT i.Ind_Name, i.Ind_Nature, i.Ind_Status, i.Coverd_Area, o.OwnName, o.CNIC, o.Mobile, o.Email, o.Address, p.plot_number, p.Location, p.Plot_Status, p.Area FROM industries i JOIN plot_ownership po ON i.plot_ID = po.plot_id JOIN OwnerTable o ON po.owner_id = o.id JOIN Plots p ON i.plot_ID = p.ID where i.id = {indid};"
    
    industries = {}
    cursor.execute(industry_query)
    industries = cursor.fetchall()
   
    print(industries[0])
    generate_report(industries[0],indid)


# Function to create the PDF report
def generate_report(industry,indusid):
    global indid
    cursor, con = db.database_connect()
    # Create PDF
    print(industry)
    pdf_filename = "Details_Report.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=A4)
    elements = []
    ##################
    custom_stylef_for_cell = ParagraphStyle(
    name="custom_stylef_for_cell",
    fontName="Helvetica",  # Change the font (e.g., Helvetica, Times-Roman, Courier)
    fontSize=12,  # Font size
    leading=10,  # Line spacing (leading is space between lines)
    spaceAfter=10,  # Space after the paragraph
    )
    custom_stylef_for_cell.alignment = 0
    ###################3
    custom_stylef_for_cell1 = ParagraphStyle(
    name="custom_stylef_for_cell1",
    fontName="Helvetica",  # Change the font (e.g., Helvetica, Times-Roman, Courier)
    fontSize=7,  # Font size
    leading=2,  # Line spacing (leading is space between lines)
    spaceAfter=2,  # Space after the paragraph
    )
    custom_stylef_for_cell1.alignment = 0
    ###########################
    custom_style = ParagraphStyle(
    name="CustomStyle",
    fontName="Helvetica",  # Change the font (e.g., Helvetica, Times-Roman, Courier)
    fontSize=12,  # Font size
    leading=10,  # Line spacing (leading is space between lines)
    spaceAfter=10,  # Space after the paragraph
    )
    custom_style.alignment = 0
    ##############
    custom_style_bulits = ParagraphStyle(
    name="CustomStyle",
    fontName="Helvetica",  # Change the font (e.g., Helvetica, Times-Roman, Courier)
    fontSize=10,  # Font size
    leading=15,  # Line spacing (leading is space between lines)
    spaceAfter=15,  # Space after the paragraph
    )
    custom_style_bulits.alignment = 0
    custom_style_bulits.leftIndent = 50
    # Add industry, owner, and plot details
    styles = getSampleStyleSheet()
    elements.append(Paragraph(f"<b> 👉 THIS REPORT PRESENTS THE FOLLOWING KEY INFORMATION :-</b><br/>",custom_style))
    startpar = f"""        1. INDUSTRY BASIC INFORMATION<br/>
                           2. OWNER AND PLOT DETAILS<br/>
                           3. INDUSTRY OUTSTANDING DUES<br/>
                           4. PAYMENT AGAINST EACH HEAD<br/>
                           5. INDUSTRY PAYMENTS RECORD<br/>
                           6. INDUSTRY OPERATIONS DETAILS<br/>
                """
    elements.append(Paragraph(startpar,custom_style_bulits))
    # Industry Details Data In Table
    ind_data = [
        [Paragraph(f'<b>Title</b>', custom_stylef_for_cell), Paragraph('Details', custom_stylef_for_cell)],
        [Paragraph(f'<b>Industry Name:</b>', custom_stylef_for_cell),Paragraph(f"{industry[0]}",custom_stylef_for_cell)],
        [Paragraph(f'<b>Industry Nature:</b>', custom_stylef_for_cell),Paragraph(f"{industry[1]}",custom_stylef_for_cell)],
        [Paragraph(f'<b>Industry Status:</b>', custom_stylef_for_cell),Paragraph(f"{industry[2]}",custom_stylef_for_cell)],
        [Paragraph(f'<b>Covered Area:</b>', custom_stylef_for_cell),Paragraph(f"{industry[3]} Acre",custom_stylef_for_cell)]
    ]
 

    balance_table = Table(ind_data)
    balance_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),              # Space inside the left of the cells
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),             # Space inside the right of the cells
        ('TOPPADDING', (0, 0), (-1, -1), 5),                # Space inside the top of the cells
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),             # Space inside the bottom of the cells
    ]))
    
    elements.append(Paragraph(f"<b>1. INDUSTRY BASIC INFORMATION</b><br/>",custom_style))
    elements.append(balance_table)
    elements.append(Spacer(1, 24))
    elements.append(Paragraph(f"<b>2. OWNER AND PLOT DETAILS</b><br/>",custom_style))
    # owner Details Data In Table
    owner_data = [
        [Paragraph(f'<b>Owner Details</b>', custom_stylef_for_cell), Paragraph('<b>Plot Details</b>', custom_stylef_for_cell)],
        [Paragraph(f"<b>Owner Name:</b> {industry[4]}",custom_stylef_for_cell), Paragraph(f"<b>Plot Number:</b> {industry[9]}", custom_stylef_for_cell)],
        [Paragraph(f"<b>CNIC:</b> {industry[5]}",custom_stylef_for_cell),Paragraph(f"<b>Location:</b> {industry[10]}",custom_stylef_for_cell)],
        [Paragraph(f"<b>Mobile:</b> {industry[6]}",custom_stylef_for_cell),Paragraph(f"<b>Plot Status:</b> {industry[11]}",custom_stylef_for_cell)],
        [Paragraph(f"<b>Email:</b> {industry[7]}",custom_stylef_for_cell),Paragraph(f"<b>Plot Area:</b> {industry[12]} Acre",custom_stylef_for_cell)],
        [Paragraph(f"<b>Address:</b> {industry[8]}",custom_stylef_for_cell),Paragraph(f"<b>Coverd Area :</b> {industry[3]} Acre",custom_stylef_for_cell)]
    ]
 

    owner_table = Table(owner_data)
    owner_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),              # Space inside the left of the cells
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),             # Space inside the right of the cells
        ('TOPPADDING', (0, 0), (-1, -1), 5),                # Space inside the top of the cells
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),             # Space inside the bottom of the cells
    ]))
    
    elements.append(owner_table)
    elements.append(Spacer(1, 24))

    elements.append(Spacer(1, 12))

    # Fetch industry balance and budget head data
    balance_query = f"SELECT bh.budget_head_name, b.balance, b.max_balance FROM balance b JOIN budget_heads bh ON b.budget_head_id = bh.budget_head_id WHERE b.industry_id = {indusid} and b.balance <> 0;"
    cursor.execute(balance_query)
    balances = cursor.fetchall()
    if balances:
        # Convert balance data to DataFrame for chart generation
        balance_df = pd.DataFrame(balances)



        # Save chart as an image (PDF-compatible)
    # chart_image = chart.to_image(format='png')

        # Add chart to PDF
    

        elements.append(Paragraph(f"<b>3. INDUSTRY OUTSTANDING DUES</b><br/>",custom_style))
        # Display balance data in table format
        outstandingamount = 0
        balance_table_data = [[Paragraph(f'<b>Budget Head</b>',custom_stylef_for_cell),Paragraph(f'<b>Balance</b>',custom_stylef_for_cell)]]
        for balance in balances:
            balance_table_data.append([Paragraph(balance[0],custom_stylef_for_cell),Paragraph(f"{balance[1]}",custom_stylef_for_cell)])
            outstandingamount = outstandingamount + balance[1]
        balance_table_data.append([Paragraph(f'<b>Total Outstanding Dues</b>',custom_stylef_for_cell),Paragraph(f'<b>{outstandingamount}</b>',custom_stylef_for_cell)])
        balance_table = Table(balance_table_data)
        balance_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),              # Space inside the left of the cells
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),             # Space inside the right of the cells
            ('TOPPADDING', (0, 0), (-1, -1), 5),                # Space inside the top of the cells
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),             # Space inside the bottom of the cells
        ]))
        elements.append(balance_table)
####################################################3
       
    # Fetch industry Payments and budget head data
    payments_query = f"""
                    SELECT 
                        bh.budget_head_name, 
                        SUM(p.amount)
                    FROM 
                        payments p
                    JOIN 
                        budget_heads bh ON p.budget_head_id = bh.budget_head_id
                    where p.industry_id = {indusid} AND p.amount <> 0
                    GROUP BY 
                        bh.budget_head_name;
                    """
    cursor.execute(payments_query)
    payments = cursor.fetchall()
   # chart_image = chart.to_image(format='png')

    # Add chart to PDF
    totalpyments = 0
    elements.append(Spacer(1, 24))
    elements.append(Paragraph(f"<b>4. PAYMENT AGAINST EACH HEAD</b><br/>",custom_style))
    # Display balance data in table format
    payments_table_data = [[Paragraph(f'<b>Budget Head</b>',custom_stylef_for_cell),Paragraph(f'<b>Paid Amount</b>',custom_stylef_for_cell)]]
    for payment in payments:
        payments_table_data.append([Paragraph(payment[0],custom_stylef_for_cell),Paragraph(f"{payment[1]}",custom_stylef_for_cell)])
        totalpyments = totalpyments + payment[1]
    payments_table_data.append([Paragraph(f'<b>Grand Total</b>',custom_stylef_for_cell),Paragraph(f'<b>{totalpyments}</b>',custom_stylef_for_cell)])
    payment_table = Table(payments_table_data)
    payment_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),              # Space inside the left of the cells
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),             # Space inside the right of the cells
        ('TOPPADDING', (0, 0), (-1, -1), 5),                # Space inside the top of the cells
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),             # Space inside the bottom of the cells
    ]))
    elements.append(payment_table)
   
# End of Payment Summary aganist each budget head


####################################################3
     
    # Fetch industry Payments and budget head data
    payments_query = f"select b.budget_head_name,p.amount,payment_date from payments p join budget_heads b on p.budget_head_id = b.budget_head_id where industry_id={indusid};"
    cursor.execute(payments_query)
    payments = cursor.fetchall()
   # chart_image = chart.to_image(format='png')

    # Add chart to PDF
    totalpyments = 0
    elements.append(Spacer(1, 24))
    elements.append(Paragraph(f"<b>5. INDUSTRY PAYMENTS RECORD</b><br/>",custom_style))
    # Display balance data in table format
    payments_table_data = [[Paragraph(f'<b>Budget Head</b>',custom_stylef_for_cell),Paragraph(f'<b>Paid Amount</b>',custom_stylef_for_cell),Paragraph(f'<b>Payment Date</b>',custom_stylef_for_cell)]]
    for payment in payments:
        payments_table_data.append([Paragraph(payment[0],custom_stylef_for_cell),Paragraph(f"{payment[1]}",custom_stylef_for_cell),Paragraph(f"{payment[2]}",custom_stylef_for_cell)])
        totalpyments = totalpyments + payment[1]
    payments_table_data.append([Paragraph(f'<b>Grand Total</b>',custom_stylef_for_cell),Paragraph(f'<b>{totalpyments}</b>',custom_stylef_for_cell),''])
    payment_table = Table(payments_table_data)
    payment_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),              # Space inside the left of the cells
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),             # Space inside the right of the cells
        ('TOPPADDING', (0, 0), (-1, -1), 5),                # Space inside the top of the cells
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),             # Space inside the bottom of the cells
    ]))
    elements.append(payment_table)
#########################################################    
    elements.append(Spacer(1, 24))

    # Fetch industry audit data
    audit_query = f"SELECT changed_field, old_value, new_value, changed_at FROM industries_audit WHERE industry_id = {indusid};"
    cursor.execute(audit_query)
    audits = cursor.fetchall()

    # Display industry audit details in a table
    audit_table_data = [[Paragraph('<b>Changed Field</b>',custom_stylef_for_cell), Paragraph('<b>Old Value</b>',custom_stylef_for_cell), Paragraph('<b>New Value</b>',custom_stylef_for_cell), Paragraph('<b>Changed At</b>',custom_stylef_for_cell)]]
    for audit in audits:
        audit_table_data.append([audit[0], audit[1], audit[2], audit[3]])

    audit_table = Table(audit_table_data)
    audit_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(Paragraph(f"<b>6. INDUSTRY OPERATIONS DETAILS</b><br/>",custom_style))
    elements.append(audit_table)
#############################################################################

    # Build the PDF
    doc.build(elements,onFirstPage=add_header_footer, onLaterPages=add_header_footer)
    print(f"Report generated: {pdf_filename}")

# Generate report for each industry
#industrydata(112)
# Close the database connection


