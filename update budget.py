import mysql.connector
from datetime import datetime
from functions import calculate_maintenance_price
# Database connection details
db_config = {
    'user': 'root',
    'password': 'asad@123',
    'host': 'localhost',
    'database': 'kpezdmc_version1'
}

# Establish database connection
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

# Specify the budget head (e.g., Maintenance, Bore Hole, AGR, etc.)
budget_head_name = 'AGR'

# Get the budget_head_id for the specified budget head
cursor.execute("SELECT budget_head_id FROM budget_heads WHERE budget_head_name = %s", (budget_head_name,))
budget_head_id = cursor.fetchone()
print(budget_head_id)
if budget_head_id is None:
    cursor.execute("Select budget_head_id from budget_heads order by budget_head_id desc limit 1")
    lastid = cursor.fetchone()
    lastid1 = lastid[0] + 1
    budget_head_id = lastid1
    print(lastid1)
    cursor.execute(
        """
        INSERT INTO budget_heads(budget_head_id,budget_head_name)
        VALUES (%s, %s)
        """,
        (lastid1,budget_head_name)
    )
    connection.commit()
elif budget_head_id:
    budget_head_id = budget_head_id[0]
else:
    print("Database Error")
    exit()

# Fetch all industries
fetchall = """
            select 
                p.Area,
                o.ownname,
                i.ind_name,
                p.id,o.id,
                i.id
            from 
                plots p
            join
                plot_ownership po
            on 
                p.id = po.plot_id
            join
                ownertable o
            on 
                o.id = po.owner_id
            left join
                industries i
            on 
                i.plot_id = p.id
            where 
	            i.ind_name is not null
            order by 
                i.created_at desc;
            """
cursor.execute(fetchall)
industries = cursor.fetchall()

# Loop through each industry
for industry in industries:
    coverd_area,ownername,industryname,plotid,ownerid,industryid = industry
    #print(industry)
    # Check if the industry already has a balance entry for the specified budget head
    if industryid is None:
        industryid = 0
    balance = f"SELECT balance_id, balance FROM balance WHERE ((owner_id = {ownerid} and plot_id = {plotid}) or (industry_id = {industryid})) AND budget_head_id = {budget_head_id};"
    cursor.execute(balance)
 
    existing_balance = cursor.fetchone()
    print(industry)
    # Example logic for calculating the balance based on covered area (you can modify this logic)
    #new_balance = coverd_area * 100  # Placeholder for balance calculation based on area
    new_balance = 12000
    # Get the current datetime
    now = datetime.now()

    if existing_balance:
        # Update the balance if the record exists
        balanceid, current_balance = existing_balance
        updatequery = """
            UPDATE balance 
            SET balance = %s,update_at = %s 
            WHERE balance_id = %s
            """
        cursor.execute(updatequery,(new_balance,now,balanceid))
        print(f"Updated balance for industry {industryid} with budget head {budget_head_name}.")
    else:
        # Insert a new record if no balance entry exists for the industry
        cursor.execute(
            """
            INSERT INTO balance (owner_id, plot_id, industry_id, budget_head_id, balance, max_balance, update_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (ownerid, plotid, industryid, budget_head_id, new_balance, new_balance, now)  # Assuming owner_id and plot_id are not relevant here
        )
        print(f"Inserted new balance record for industry {industryid} with budget head {budget_head_name}.")

# Commit the transaction
connection.commit()

# Close the cursor and connection
cursor.close()
connection.close()
