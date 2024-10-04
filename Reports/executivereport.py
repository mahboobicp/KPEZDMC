import mysql.connector
import pandas as pd
import altair as alt
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from decimal import Decimal

# Database connection
cnx = mysql.connector.connect(
    host='localhost',        # Your MySQL host
        database='kpezdmc_version1', # Your database name
        user='root',     # Your MySQL username
        password='asad@123'  # Your MySQL password
)

# Create a cursor object
cursor = cnx.cursor()

# Fetch total industries and their statuses
query = """
 SELECT Ind_Status, COUNT(*) as count, 'Nowshera Economic Zone' AS zone
    FROM industries
    WHERE plot_id IN (SELECT id FROM Plots WHERE zone = 'NEZ Old')
    GROUP BY Ind_Status
    UNION ALL
    SELECT Ind_Status, COUNT(*) as count, 'Nowshera Economic Zone Ext' AS zone
    FROM industries
    WHERE plot_id IN (SELECT id FROM Plots WHERE zone = 'NEZ Extenssion')
    GROUP BY Ind_Status;
"""
cursor.execute(query)
industries_data = cursor.fetchall()
industries_df = pd.DataFrame(industries_data, columns=['Ind_Status', 'count', 'zone'])

# Convert Decimal columns to float
industries_df['count'] = industries_df['count'].astype(float)

# Create a chart for industry status
chart_industry_status = alt.Chart(industries_df).mark_bar().encode(
    x='Ind_Status',
    y='count',
    color='zone'
).properties(title='Industries Status by Zone')

# Save the industry status chart
chart_industry_status.save('industry_status_chart.html')
chart_industry_status.save('industry_status_chart.png', format='png')

# Fetch payment details for each budget head in the current year
query_payments = """
SELECT bh.budget_head_name, SUM(p.amount) as total_amount
FROM payments p
JOIN budget_heads bh ON p.industry_id = bh.budget_head_id
WHERE YEAR(p.payment_date) = YEAR(CURRENT_DATE)
GROUP BY bh.budget_head_name;
"""
cursor.execute(query_payments)
payments_data = cursor.fetchall()
payments_df = pd.DataFrame(payments_data, columns=['Budget Head', 'Total Amount'])

# Convert Decimal columns to float
payments_df['Total Amount'] = payments_df['Total Amount'].astype(float)

# Create a chart for payments by budget head
chart_payments = alt.Chart(payments_df).mark_bar().encode(
    x='Budget Head',
    y='Total Amount'
).properties(title='Payments by Budget Head in Current Year')

# Save the payments chart
chart_payments.save('payments_chart.html')
chart_payments.save('payments_chart.png', format='png')

# Fetch long outstanding dues
query_outstanding = """
SELECT bh.budget_head_name, SUM(b.balance) as outstanding_balance
FROM balance b
JOIN budget_heads bh ON b.budget_head_id = bh.budget_head_id
WHERE b.balance > 0
GROUP BY bh.budget_head_name;
"""
cursor.execute(query_outstanding)
outstanding_data = cursor.fetchall()
outstanding_df = pd.DataFrame(outstanding_data, columns=['Budget Head', 'Outstanding Balance'])

# Convert Decimal columns to float
outstanding_df['Outstanding Balance'] = outstanding_df['Outstanding Balance'].astype(float)

# Create a chart for outstanding dues
chart_outstanding = alt.Chart(outstanding_df).mark_bar().encode(
    x='Budget Head',
    y='Outstanding Balance'
).properties(title='Long Outstanding Dues by Budget Head')

# Save the outstanding dues chart
chart_outstanding.save('outstanding_chart.html')
chart_outstanding.save('outstanding_chart.png', format='png')

# Create a PDF report in landscape orientation
pdf_file = 'executive_report.pdf'
c = canvas.Canvas(pdf_file, pagesize=landscape(A4))
width, height = landscape(A4)

# Add report title
c.setFont("Helvetica-Bold", 16)
c.drawString(50, height - 50, "Executive Report for KPEZDMC")

# Add industry status section
c.setFont("Helvetica-Bold", 14)
c.drawString(50, height - 100, "Industries Status by Zone")
c.drawImage('industry_status_chart.png', 50, height - 300, width=800, height=400)

# Add payments section
c.setFont("Helvetica-Bold", 14)
c.drawString(50, height - 750, "Payments by Budget Head in Current Year")
c.drawImage('payments_chart.png', 50, height - 1150, width=800, height=400)

# Add outstanding dues section
c.setFont("Helvetica-Bold", 14)
c.drawString(50, height - 1550, "Long Outstanding Dues by Budget Head")
c.drawImage('outstanding_chart.png', 50, height - 1950, width=800, height=400)

# Finalize the PDF
c.save()

# Clean up
cursor.close()
cnx.close()

print("Report generated successfully!")
