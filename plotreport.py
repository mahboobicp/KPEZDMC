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



def plotdata(indid):
    cursor,con = db.database_connect()

    # Query to fetch industry details, owner details, and plot details
    industry_query = f"SELECT i.Ind_Name, i.Ind_Nature, i.Ind_Status, i.Coverd_Area, o.OwnName, o.CNIC, o.Mobile, o.Email, o.Address, p.id, p.Location, p.Plot_Status, p.Area FROM industries i JOIN plot_ownership po ON i.plot_ID = po.plot_id JOIN OwnerTable o ON po.owner_id = o.id JOIN Plots p ON i.plot_ID = p.ID where p.id = {indid};"
    
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
    pdf_filename = "Plot_Details_Report.pdf"
    doc = SimpleDocTemplate(pdf_filename,pagesize=landscape(A4))
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
    fontSize=8,  # Font size
    leading=7,  # Line spacing (leading is space between lines)
    spaceAfter=8,  # Space after the paragraph
    )
    custom_stylef_for_cell1.alignment = 0
    ###########################
    custom_style = ParagraphStyle(
    name="CustomStyle",
    fontName="Helvetica",  # Change the font (e.g., Helvetica, Times-Roman, Courier)
    fontSize=14,  # Font size
    leading=10,  # Line spacing (leading is space between lines)
    spaceAfter=10,  # Space after the paragraph
    )
    custom_style.alignment = 1

#############################################################################
    elements.append(Spacer(1, 24))

    # Fetch industry audit data
    audit_query = f"SELECT changed_field, old_value, new_value, changed_at FROM industries_audit WHERE industry_id = {indusid};"
    audit_plot =f"""
                SELECT 
                    apo.plot_id,
                    apo.po_status,
                    apo.start_date,
                    old_owner.OwnName AS old_owner_name,
                    old_owner.CNIC AS old_owner_cnic,
                    apo.end_date,
                    apo.change_type,
                    new_owner.OwnName AS new_owner_name,
                    new_owner.CNIC AS new_owner_cnic,
                    apo.changed_at
                FROM 
                    audit_plot_ownership apo
                LEFT JOIN 
                    OwnerTable old_owner ON apo.owner_id = old_owner.id  -- Get old owner details
                LEFT JOIN 
                    OwnerTable new_owner ON apo.new_owner_id = new_owner.id  -- Get new owner details
                WHERE
                    plot_id = {indusid} AND apo.new_owner_id IS NOT NULL
                ORDER BY 
                    apo.plot_id DESC;
                """
    cursor.execute(audit_plot)
    audits_plot = cursor.fetchall()

    # Display industry audit details in a table
    audit_plot_table_data = [[Paragraph('<b>Plot ID</b>',custom_stylef_for_cell1), Paragraph('<b>Plot Status</b>',custom_stylef_for_cell1),
                              Paragraph('<b>Allotment Date</b>',custom_stylef_for_cell1), Paragraph('<b>Old Owner</b>',custom_stylef_for_cell1),
                              Paragraph('<b>Owner CNIC</b>',custom_stylef_for_cell1),Paragraph('<b>End Date</b>',custom_stylef_for_cell1),
                              Paragraph('<b>New Status</b>',custom_stylef_for_cell1),Paragraph('<b>New Owner</b>',custom_stylef_for_cell1),
                              Paragraph('<b>Owner CNIC</b>',custom_stylef_for_cell1),Paragraph('<b>Changed Date</b>',custom_stylef_for_cell1)]]
    for audit in audits_plot:
        audit_plot_table_data.append([audit[0], audit[1], audit[2], audit[3],audit[4],audit[5],audit[6],audit[7],audit[8],audit[9]])

    audit_plot_table = Table(audit_plot_table_data)
    audit_plot_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    #canvas.saveState()
    #canvas.setPageSize(landscape(A4))
    elements.append(Paragraph(f"<b>Plot Allotment Details Details</b><br/>",custom_style))
    elements.append(audit_plot_table)

    # Build the PDF
    doc.build(elements,onFirstPage=add_header_footer, onLaterPages=add_header_footer)
    print(f"Report generated: {pdf_filename}")

# Generate report for each industry
#industrydata(112)
# Close the database connection


