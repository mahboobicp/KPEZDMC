import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import mysql.connector
from io import BytesIO

# Database connection
def fetch_balance_data():
    # Connect to the database
    connection = mysql.connector.connect(
           host='localhost',        # Your MySQL host
            database='kpezdmc_version1', # Your database name
            user='root',     # Your MySQL username
            password='asad@123'  # Your MySQL password
    )
    
    cursor = connection.cursor()
    query = """
    SELECT budget_heads.budget_head_name, SUM(balance.balance)
    FROM balance
    JOIN budget_heads ON balance.budget_head_id = budget_heads.budget_head_id
    GROUP BY balance.budget_head_id;
    """
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return data

# Generate a bar chart with the data
def create_balance_chart(data):
    budget_heads = [item[0] for item in data]
    balances = [item[1] for item in data]

    plt.figure(figsize=(6, 4))
    plt.bar(budget_heads, balances, color='skyblue')
    plt.xlabel('Budget Heads')
    plt.ylabel('Total Balance')
    plt.title('Industry Balance by Budget Head')
    plt.xticks(rotation=45, ha='right')
    
    # Save chart to a BytesIO object
    chart_image = BytesIO()
    plt.tight_layout()
    plt.savefig(chart_image, format='png')
    plt.close()  # Close the plot to free memory
    
    chart_image.seek(0)
    return chart_image

# Create PDF report
def create_pdf_report():
    # Fetch data
    data = fetch_balance_data()
    
    # Create PDF document
    pdf = SimpleDocTemplate("industry_balance_report.pdf", pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    
    # Add title
    elements.append(Paragraph("Industry Balance by Budget Head", styles["Title"]))
    elements.append(Spacer(1, 12))
    
    # Generate and add chart to PDF
    chart_image = create_balance_chart(data)
    chart = Image(chart_image, 6 * inch, 4 * inch)  # Adjust the size of the chart
    elements.append(chart)
    
    # Add some space after the chart
    elements.append(Spacer(1, 24))
    
    # Build the PDF
    pdf.build(elements)

# Call the function to generate the PDF
create_pdf_report()
