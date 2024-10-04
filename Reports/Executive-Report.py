import mysql.connector
import pandas as pd  # Import pandas
import matplotlib.pyplot as plt
import seaborn as sns
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from datetime import datetime

# Connect to MySQL Database
def connect_db():
    cnx = mysql.connector.connect(
        host='localhost',        # Your MySQL host
        database='kpezdmc_version1', # Your database name
        user='root',     # Your MySQL username
        password='asad@123'  # Your MySQL password
    )
    return cnx

# Fetch Data for the Report
def fetch_data():
    cnx = connect_db()
    cursor = cnx.cursor(dictionary=True)

    # Query for total industries by zone
    cursor.execute("""
    SELECT Ind_Status, COUNT(*) as count, 'Nowshera Economic Zone' AS zone
    FROM industries
    WHERE plot_id IN (SELECT id FROM Plots WHERE zone = 'NEZ Old')
    GROUP BY Ind_Status
    UNION ALL
    SELECT Ind_Status, COUNT(*) as count, 'Nowshera Economic Zone Ext' AS zone
    FROM industries
    WHERE plot_id IN (SELECT id FROM Plots WHERE zone = 'NEZ Extenssion')
    GROUP BY Ind_Status;
    """)
    industries_by_zone = cursor.fetchall()

    # Query for payments per budget head in current year
    cursor.execute("""
    SELECT bh.budget_head_name, SUM(p.amount) AS total_payment
    FROM payments p
    JOIN budget_heads bh ON p.budget_head_id = bh.budget_head_id
    WHERE YEAR(p.payment_date) = YEAR(CURDATE())
    GROUP BY bh.budget_head_name;
    """)
    payments_by_budget_head = cursor.fetchall()

    # Query for long outstanding dues (balance <= 0)
    cursor.execute("""
    SELECT i.Ind_Name, ba.balance, ba.max_balance
    FROM balance ba
    JOIN industries i ON ba.industry_id = i.Id
    WHERE ba.balance <= 0;
    """)
    outstanding_dues = cursor.fetchall()

    cursor.close()
    cnx.close()
    
    # Convert lists of dictionaries to DataFrames
    industries_df = pd.DataFrame(industries_by_zone)
    payments_df = pd.DataFrame(payments_by_budget_head)
    outstanding_dues_df = pd.DataFrame(outstanding_dues)

    return industries_df, payments_df, outstanding_dues_df

# Plot Chart Functions
def plot_industries_by_zone(data):
    plt.figure(figsize=(10, 6))
    sns.barplot(x='zone', y='count', hue='Ind_Status', data=data)
    plt.title('Number of Industries by Zone and Status')
    plt.savefig('industries_by_zone.png', bbox_inches='tight')
    plt.close()  # Close the figure to avoid display

def plot_payments_by_budget_head(data):
    plt.figure(figsize=(8, 5))
    sns.barplot(x='budget_head_name', y='total_payment', data=data)
    plt.title('Payments by Budget Head (Current Year)')
    plt.xticks(rotation=45)
    plt.savefig('payments_by_budget_head.png', bbox_inches='tight')
    plt.close()

def plot_outstanding_dues(data):
    plt.figure(figsize=(8, 5))
    sns.barplot(x='Ind_Name', y='balance', data=data)
    plt.title('Long Outstanding Dues (Balance <= 0)')
    plt.xticks(rotation=45)
    plt.savefig('outstanding_dues.png', bbox_inches='tight')
    plt.close()

# Generate PDF Report
def generate_report(industries_df, payments_df, outstanding_dues_df):
    c = canvas.Canvas("Executive_Report.pdf", pagesize=A4)
    width, height = A4

    # Add Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(1*inch, height - 1*inch, "KPEZDMC Executive Report")
    c.setFont("Helvetica", 12)
    c.drawString(1*inch, height - 1.3*inch, f"Date: {datetime.now().strftime('%Y-%m-%d')}")

    # Insert industries by zone chart
    plot_industries_by_zone(industries_df)
    c.drawImage('industries_by_zone.png', 1*inch, height - 4*inch, width=6*inch, height=3*inch)

    # Insert payments by budget head chart
    plot_payments_by_budget_head(payments_df)
    c.drawImage('payments_by_budget_head.png', 1*inch, height - 8*inch, width=6*inch, height=3*inch)

    # Insert outstanding dues chart
    plot_outstanding_dues(outstanding_dues_df)
    c.drawImage('outstanding_dues.png', 1*inch, height - 12*inch, width=6*inch, height=3*inch)

    # Save PDF
    c.showPage()
    c.save()

# Main Execution
if __name__ == "__main__":
    industries_df, payments_df, outstanding_dues_df = fetch_data()
    generate_report(industries_df, payments_df, outstanding_dues_df)
