from fpdf import FPDF
import matplotlib.pyplot as plt
from io import BytesIO
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

# Function to generate a pie chart for balance dues
def create_pie_chart(data):
    labels = [row[0] for row in data]  # Budget heads
    balances = [row[1] for row in data]  # Balances
    
    plt.figure(figsize=(3, 3))
    plt.pie(balances, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')  # Equal aspect ratio ensures pie is drawn as a circle.
    
    plt.savefig('pie_chart.png', format='png', bbox_inches='tight', dpi=150)
    plt.close()  # Close the plot to free up memory


# Function to generate PDF invoice notification
def generate_pdf():
    # Fetch data from database
    data, balance_dues = fetch_data(100)
    if not data:
        print("No data found.")
        return

    # Create FPDF object
    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_page()

    # Add company logo
    pdf.image('D:\Python\KPEZDMC\images\comlogo.png', x=10, y=8, w=33)  # Adjust path and size as needed

    # Add Industry Name and Owner Name
    industry_name, owner_name = data[0][0], data[0][1]  # Unpacking first row (assuming single industry)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(100, 10, f'Industry: {industry_name}', ln=1, align='L')
    pdf.cell(100, 10, f'Owner: {owner_name}', ln=1, align='L')

    # Add Date on the right
    pdf.set_xy(140, 10)  # Position to top right
    pdf.cell(60, 10, f'Date: {datetime.now().strftime("%d-%m-%Y")}', ln=1, align='R')

    pdf.ln(10)  # Line break

    # Add Subject Line
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(190, 10, 'Subject: Submission of Balance Dues', ln=1, align='L')

    pdf.ln(5)

    # Add Greeting and request message
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(190, 10, 'Dear Sir/Madam, \n\nWe kindly request you to submit the balance dues as per the details below.', align='L')

    pdf.ln(5)

    # Add Balance Details in Table Format
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(95, 10, 'Budget Head', border=1, align='C')
    pdf.cell(95, 10, 'Balance (Amount)', border=1, ln=1, align='C')

    pdf.set_font('Arial', '', 12)
    total_balance = 0
    for row in balance_dues:
        budget_head = row[0]
        balance = row[1]
        total_balance += balance
        pdf.cell(95, 10, budget_head, border=1, align='C')
        pdf.cell(95, 10, f'${balance:,.2f}', border=1, ln=1, align='C')

    pdf.ln(10)

    # Generate Pie Chart
    pie_chart_buffer = create_pie_chart(balance_dues)
    #pdf.image(pie_chart_buffer, x=50, y=pdf.get_y(), w=100, h=100)  # Insert pie chart
    pdf.image('pie_chart.png', x=50, y=pdf.get_y(), w=100, h=100)
    pdf.ln(110)  # Line break after pie chart

    # Closing Message with Bank Details
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(190, 10, 'We kindly request you to submit the balance dues at your earliest convenience. '
                            'The payment can be made to the following account:\n\n'
                            'Account Name: Industry Payment Services\n'
                            'Account Number: 123456789\n'
                            'Bank: National Bank\n'
                            'Branch Code: 00112233', align='L')

    # Save the PDF
    pdf.output('industry_invoice.pdf')
    print("PDF generated successfully.")

# Call the function to generate the PDF
generate_pdf()
