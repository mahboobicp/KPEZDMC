import mysql.connector
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.platypus import Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import altair as alt
import pandas as pd
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


# Function to create the PDF report
def generate_zone_report():
    global indid
    cursor, con = db.database_connect()
    # Create PDF
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
    custom_style = ParagraphStyle(
    name="CustomStyle",
    fontName="Helvetica",  # Change the font (e.g., Helvetica, Times-Roman, Courier)
    fontSize=14,  # Font size
    leading=10,  # Line spacing (leading is space between lines)
    spaceAfter=10,  # Space after the paragraph
    )
    custom_style.alignment = 1
    # Add industry, owner, and plot details
    styles = getSampleStyleSheet()
    # Industry Details Data In Table
   
    extquery = """
                SELECT 
                    p.zone AS 'Zone',
                    i.Ind_Status AS 'Industry Status',
                    COUNT(i.Id) AS 'Industry Count'
                FROM industries i
                JOIN Plots p ON i.plot_ID = p.ID
                where p.zone = 'NEZ Ext'
                GROUP BY p.zone, i.Ind_Status
                ORDER BY p.zone, i.Ind_Status;
    """
    cursor.execute(extquery)
    extindustries = cursor.fetchall()

    print(extindustries[0])

    # Save chart as an image (PDF-compatible)
   # chart_image = chart.to_image(format='png')

    # Add chart to PDF
   
    exttotalindustries = 0
    elements.append(Paragraph(f"<b>NEZ Extension Industries Status</b><br/>",custom_style))
    # Display status count data in table format
    extensionstatus_table = [[Paragraph(f'<b>Industries Status</b>',custom_stylef_for_cell),Paragraph(f'<b>Industries Count</b>',custom_stylef_for_cell)]]
    for i in extindustries:
        extensionstatus_table.append([Paragraph(f"{i[1]}",custom_stylef_for_cell),Paragraph(f"{i[2]}",custom_stylef_for_cell)])
        exttotalindustries  = exttotalindustries + i[2]
      
    extensionstatus_table.append([Paragraph(f'<b>Total Industries </b>',custom_stylef_for_cell),Paragraph(f'<b>{exttotalindustries}</b>',custom_stylef_for_cell)])
    ext_table = Table(extensionstatus_table)
    ext_table.setStyle(TableStyle([
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
    elements.append(ext_table)
####################################################3
     
    nezquery = """
                SELECT 
                    p.zone AS 'Zone',
                    i.Ind_Status AS 'Industry Status',
                    COUNT(i.Id) AS 'Industry Count'
                FROM industries i
                JOIN Plots p ON i.plot_ID = p.ID
                where p.zone = 'NEZ Old'
                GROUP BY p.zone, i.Ind_Status
                ORDER BY p.zone, i.Ind_Status;
    """
    cursor.execute(nezquery)
    nezindustries = cursor.fetchall()

   

    elements.append(Paragraph(f"<b>NEZ Old Industries Status</b><br/>",custom_style))
    # Display status count data in table format
    neztotalindustries = 0
    nezensionstatus_table = [[Paragraph(f'<b>Industries Status</b>',custom_stylef_for_cell),Paragraph(f'<b>Industries Count</b>',custom_stylef_for_cell)]]
    for i in nezindustries:
        nezensionstatus_table.append([Paragraph(f"{i[1]}",custom_stylef_for_cell),Paragraph(f"{i[2]}",custom_stylef_for_cell)])
        neztotalindustries  = neztotalindustries + i[2]
      
    nezensionstatus_table.append([Paragraph(f'<b>Total Industries </b>',custom_stylef_for_cell),Paragraph(f'<b>{neztotalindustries}</b>',custom_stylef_for_cell)])
    nez_table = Table(nezensionstatus_table)
    nez_table.setStyle(TableStyle([
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
    elements.append(nez_table)
   #################################################################
     
    quarterquery = """              
                    SELECT 
                        p.zone AS 'Zone',
                        QUARTER(pay.payment_date) AS 'Quarter',
                        YEAR(pay.payment_date) AS 'Year',
                        bh.budget_head_name AS 'Budget Head',
                        SUM(pay.amount) AS 'Total Payments'
                    FROM 
                        payments pay
                    JOIN 
                        Plots p ON pay.plot_id = p.ID
                    JOIN 
                        budget_heads bh ON pay.budget_head_id = bh.budget_head_id
                    WHERE 
                        YEAR(pay.payment_date) = YEAR(CURDATE())  -- Only consider payments from the current year
                        And p.zone = 'NEZ Ext'
                    GROUP BY 
                        p.zone, YEAR(pay.payment_date), QUARTER(pay.payment_date), bh.budget_head_name
                    ORDER BY 
                        p.zone, YEAR(pay.payment_date), QUARTER(pay.payment_date), bh.budget_head_name;
    """
    cursor.execute(quarterquery)
    quarterreport = cursor.fetchall()

   
    extpayment = 0
    elements.append(Paragraph(f"<b>NEZ Ext Payments Report (Quarterly) </b><br/>",custom_style))
    # Display status count data in table format
    quarterreport_table = [[Paragraph(f'<b>Budget Head</b>',custom_stylef_for_cell),Paragraph(f'<b>Year</b>',custom_stylef_for_cell),Paragraph(f'<b>Quarter</b>',custom_stylef_for_cell),Paragraph(f'<b>Total Payment</b>',custom_stylef_for_cell)]]
    for i in quarterreport:
        quarterreport_table.append([Paragraph(f"{i[3]}",custom_stylef_for_cell),Paragraph(f"{i[2]}",custom_stylef_for_cell),Paragraph(f"{i[1]}",custom_stylef_for_cell),Paragraph(f"{i[4]}",custom_stylef_for_cell)])
        extpayment = extpayment + i[4]
    quarterreport_table.append(['','',Paragraph(f'<b>Total Payment</b>',custom_stylef_for_cell),Paragraph(f'<b>{extpayment}</b>',custom_stylef_for_cell)])
    quarter_table = Table(quarterreport_table)
    quarter_table.setStyle(TableStyle([
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
    elements.append(quarter_table)
    ###################################################################
    
    quarterquery = """              
                    SELECT 
                        p.zone AS 'Zone',
                        QUARTER(pay.payment_date) AS 'Quarter',
                        YEAR(pay.payment_date) AS 'Year',
                        bh.budget_head_name AS 'Budget Head',
                        SUM(pay.amount) AS 'Total Payments'
                    FROM 
                        payments pay
                    JOIN 
                        Plots p ON pay.plot_id = p.ID
                    JOIN 
                        budget_heads bh ON pay.budget_head_id = bh.budget_head_id
                    WHERE 
                        YEAR(pay.payment_date) = YEAR(CURDATE())  -- Only consider payments from the current year
                        And p.zone = 'NEZ Old'
                    GROUP BY 
                        p.zone, YEAR(pay.payment_date), QUARTER(pay.payment_date), bh.budget_head_name
                    ORDER BY 
                        p.zone, YEAR(pay.payment_date), QUARTER(pay.payment_date), bh.budget_head_name;
    """
    cursor.execute(quarterquery)
    quarterreport = cursor.fetchall()

   
    nezpayment = 0
    elements.append(Paragraph(f"<b>NEZ Old Payments Report (Quarterly) </b><br/>",custom_style))
    # Display status count data in table format
    quarterreport_table = [[Paragraph(f'<b>Budget Head</b>',custom_stylef_for_cell),Paragraph(f'<b>Year</b>',custom_stylef_for_cell),Paragraph(f'<b>Quarter</b>',custom_stylef_for_cell),Paragraph(f'<b>Total Payment</b>',custom_stylef_for_cell)]]
    for i in quarterreport:
        quarterreport_table.append([Paragraph(f"{i[3]}",custom_stylef_for_cell),Paragraph(f"{i[2]}",custom_stylef_for_cell),Paragraph(f"{i[1]}",custom_stylef_for_cell),Paragraph(f"{i[4]}",custom_stylef_for_cell)])
        nezpayment = nezpayment + i[4]
    quarterreport_table.append(['','',Paragraph(f'<b>Total Payment</b>',custom_stylef_for_cell),Paragraph(f'<b>{nezpayment}</b>',custom_stylef_for_cell)])
    quarter_table = Table(quarterreport_table)
    quarter_table.setStyle(TableStyle([
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
    elements.append(quarter_table)
    ############################################
    
    quarterquery = """              
                    SELECT 
                        p.zone AS 'Zone',
                        YEAR(pay.payment_date) AS 'Year',
                        bh.budget_head_name AS 'Budget Head',
                        SUM(pay.amount) AS 'Total Payments'
                    FROM 
                        payments pay
                    JOIN 
                        Plots p ON pay.plot_id = p.ID
                    JOIN 
                        budget_heads bh ON pay.budget_head_id = bh.budget_head_id
                    WHERE 
                        p.zone = 'NEZ Ext'
                    GROUP BY 
                        p.zone, YEAR(pay.payment_date), bh.budget_head_name
                    ORDER BY 
                        p.zone, YEAR(pay.payment_date), bh.budget_head_name;
                    """
    cursor.execute(quarterquery)
    quarterreport = cursor.fetchall()

   
    extyearlypayment = 0
    elements.append(Paragraph(f"<b>NEZ Ext Payments Report (Yearly) </b><br/>",custom_style))
    # Display status count data in table format
    yearlyreport_table = [[Paragraph(f'<b>Budget Head</b>',custom_stylef_for_cell),Paragraph(f'<b>Year</b>',custom_stylef_for_cell),Paragraph(f'<b>Total Payment</b>',custom_stylef_for_cell)]]
    for i in quarterreport:
        yearlyreport_table.append([Paragraph(f"{i[2]}",custom_stylef_for_cell),Paragraph(f"{i[1]}",custom_stylef_for_cell),Paragraph(f"{i[3]}",custom_stylef_for_cell)])
        extyearlypayment = extyearlypayment + i[3]
    yearlyreport_table.append(['',Paragraph(f'<b>Total Payment</b>',custom_stylef_for_cell),Paragraph(f'<b>{extyearlypayment}</b>',custom_stylef_for_cell)])
    yearly_table = Table(yearlyreport_table)
    yearly_table.setStyle(TableStyle([
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
    elements.append(yearly_table)
    #########################################################
    
    quarterquery = """              
                    SELECT 
                        p.zone AS 'Zone',
                        YEAR(pay.payment_date) AS 'Year',
                        bh.budget_head_name AS 'Budget Head',
                        SUM(pay.amount) AS 'Total Payments'
                    FROM 
                        payments pay
                    JOIN 
                        Plots p ON pay.plot_id = p.ID
                    JOIN 
                        budget_heads bh ON pay.budget_head_id = bh.budget_head_id
                    WHERE 
                        p.zone = 'NEZ Old'
                    GROUP BY 
                        p.zone, YEAR(pay.payment_date), bh.budget_head_name
                    ORDER BY 
                        p.zone, YEAR(pay.payment_date), bh.budget_head_name;
                    """
    cursor.execute(quarterquery)
    quarterreport = cursor.fetchall()

   
    extyearlypayment = 0
    elements.append(Paragraph(f"<b>NEZ Old Payments Report (Yearly) </b><br/>",custom_style))
    # Display status count data in table format
    yearlyreport_table = [[Paragraph(f'<b>Budget Head</b>',custom_stylef_for_cell),Paragraph(f'<b>Year</b>',custom_stylef_for_cell),Paragraph(f'<b>Total Payment</b>',custom_stylef_for_cell)]]
    for i in quarterreport:
        yearlyreport_table.append([Paragraph(f"{i[2]}",custom_stylef_for_cell),Paragraph(f"{i[1]}",custom_stylef_for_cell),Paragraph(f"{i[3]}",custom_stylef_for_cell)])
        extyearlypayment = extyearlypayment + i[3]
    yearlyreport_table.append(['',Paragraph(f'<b>Total Payment</b>',custom_stylef_for_cell),Paragraph(f'<b>{extyearlypayment}</b>',custom_stylef_for_cell)])
    yearly_table = Table(yearlyreport_table)
    yearly_table.setStyle(TableStyle([
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
    elements.append(yearly_table)
    # Build the PDF
    doc.build(elements,onFirstPage=add_header_footer, onLaterPages=add_header_footer)
    print(f"Report generated: {pdf_filename}")

# Generate report for each industry
#industrydata(112)
# Close the database connection

#generate_zone_report()
