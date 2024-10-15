import mysql.connector
import pandas as pd

# Connect to the MySQL database
conn = mysql.connector.connect(
    host='localhost',        # Your MySQL host
    database='kpezdmc_version1', # Your database name
    user='root',     # Your MySQL username
    password='asad@123'  # Your MySQL password
)

# The SQL query from earlier
query = """
SELECT 
    i.Ind_Name AS Industry_Name,
    o.OwnName AS Owner_Name,
    i.Coverd_Area AS Area,
    i.Ind_Status AS Industry_Status,
    bh.budget_head_name AS Budget_Head_Name,
    b.balance AS Balance,
    b.max_balance AS Max_Balance,
    b.update_at AS Last_Updated
FROM industries i
JOIN industry_ownerships io ON i.Id = io.industry_id
JOIN OwnerTable o ON io.owner_id = o.id
LEFT JOIN balance b ON i.Id = b.industry_id
LEFT JOIN budget_heads bh ON b.budget_head_id = bh.budget_head_id
ORDER BY i.Ind_Name, bh.budget_head_name;
"""

# Execute the query and read the results into a pandas DataFrame
df = pd.read_sql(query, conn)

# Export the DataFrame to an Excel file
output_file = 'industry_data_report.xlsx'
df.to_excel(output_file, index=False, engine='openpyxl')  # Saves without row indices

# Close the connection
conn.close()

print(f"Data exported successfully to {output_file}")
