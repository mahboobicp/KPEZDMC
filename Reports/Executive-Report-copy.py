import mysql.connector
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# MySQL connection setup
connection = mysql.connector.connect(
    host='localhost',        # Your MySQL host
    database='kpezdmc_version1', # Your database name
    user='root',     # Your MySQL username
    password='asad@123'  # Your MySQL password
)

cursor = connection.cursor()

# Query for industries and balance data
cursor.execute("""
    SELECT i.Ind_Name, b.balance, bh.budget_head_name
    FROM industries i
    JOIN balance b ON i.Id = b.industry_id
    JOIN budget_heads bh ON b.budget_head_id = bh.budget_head_id
""")
data = cursor.fetchall()

# Create a DataFrame for ease of plotting
df = pd.DataFrame(data, columns=['Industry Name', 'Balance', 'Budget Head'])

# Plotting the data
# Create a bar plot using Seaborn
plt.figure(figsize=(10, 6))
sns.barplot(data=df, x='Industry Name', y='Balance', hue='Budget Head')

# Customize the plot
plt.title('Industry Balance Across Budget Heads')
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

# Save the plot to a file
plt.savefig("industry_balance_chart.png")

# Display the plot
plt.show()

# Close the cursor and connection
cursor.close()
connection.close()
