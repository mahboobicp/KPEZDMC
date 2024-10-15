import customtkinter as ct
import tkinter 
from PIL import Image
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry
import mysql.connector
from datetime import datetime
from mysql.connector import Error

def database_connect():
    try:
    # Establish the connection
        connection = mysql.connector.connect(
            host='localhost',        # Your MySQL host
            database='kpezdmc_version1', # Your database name
            user='root',     # Your MySQL username
            password='asad@123'  # Your MySQL password
        )

        if connection.is_connected():
            # Get the server information
            db_info = connection.get_server_info()
            print("Connected to MySQL Server version", db_info)
            
            # Create a cursor object using the cursor() method
            cursor = connection.cursor()
            return cursor , connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        messagebox.showerror("Error",f"Database Connection error : {e}")
"""  finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed") """
def calculate_maintenance_price(area_in_acres,price_per_acre):
    area_in_acres = float(area_in_acres)
    price_per_acre = float(price_per_acre)
    # 1 acre = 43,560 square feet
    SQUARE_FEET_PER_ACRE = 43560
    
    # Convert acres to square feet
    area_in_square_feet = area_in_acres * SQUARE_FEET_PER_ACRE
    
    # Calculate the price per square foot
    price_per_square_foot = price_per_acre / SQUARE_FEET_PER_ACRE
    
    # Calculate the total price of the plot
    plot_price = area_in_square_feet * price_per_square_foot
    return plot_price

def get_id(table):
    cur,con = database_connect()
    # Calculate the plot ID
    cur.execute(f"SELECT id FROM {table} ORDER BY id DESC LIMIT 1")
    result = cur.fetchone() 
    if result is None:
        # If there's no row or id is NULL, insert the specific value (e.g., 1)
        id = 100
    else:
        # If id is not NULL, get the last id and increment the value by 1
        last_id = result[0]
        id = last_id + 1
    return id
def get_balance_id(table,id):
    cur,con = database_connect()
    # Calculate the plot ID
    cur.execute(f"SELECT {id} FROM {table} ORDER BY {id} DESC LIMIT 1")
    result = cur.fetchone() 
    if result is None:
        # If there's no row or id is NULL, insert the specific value (e.g., 1)
        id = 100
    else:
        # If id is not NULL, get the last id and increment the value by 1
        last_id = result[0]
        id = last_id + 1
    return id
def get_budget_head(head):
    cur,con = database_connect()
    query = f"select budget_head_id from budget_heads where budget_head_name = '{head}';"
    cur.execute(query)
    result = cur.fetchone()
    print(query)
    print(result)
    if result is None:
        cur.execute("SELECT budget_head_id FROM budget_heads ORDER BY budget_head_id DESC LIMIT 1")
        fetch_id = cur.fetchone() 
        if fetch_id is None:
        # If there's no row or id is NULL, insert the specific value (e.g., 1)
            budget_head_id = 100
        else:
        # If id is not NULL, get the last id and increment the value by 1
            last_id = fetch_id[0]
            budget_head_id = last_id + 1
   
        #query = "insert into budget_heads(budget_head_id,budget_head_name) VALUES(%s,%s)"
        insert_query = """INSERT INTO budget_heads (budget_head_id,budget_head_name) 
                                    VALUES (%s,%s)"""
        data = (budget_head_id,head)
        cur.execute(insert_query,data)
        con.commit()
        return budget_head_id
    else:
        return result[0]


def update_balancedata_if_nature_changed(ownerid,plotid,indid):
    cur, con = database_connect()
    cur.execute("use kpezdmc_version1")
    budgetid = get_budget_head("Nature Change")
    print(f"Return ID {budgetid}")
    recorcheck = f"select balance_id from balance where industry_id = {indid} and budget_head_id = {budgetid};"
    cur.execute(recorcheck)
    result = cur.fetchone()
    print(f"Balance id {result}")
    if result is None:
         print("Not Found")
         print(f"owner id {ownerid} plot id {plotid} industry id {indid}")
         insert_query_balance = """INSERT INTO balance (balance_id,owner_id,plot_id,industry_id,budget_head_id,balance,update_at) 
                                    VALUES (%s,%s,%s,%s,%s,%s,%s)"""
        # Get plot id and owner id from tree
        # Cureent Date
         current_date = datetime.now()

        # Format the current date
         formatted_date = current_date.strftime("%Y/%m/%d %H:%M:%S")  # Example format: 2024-09-03
        # Data to be inserted
         balance_id = get_balance_id("balance","balance_id")
        # print(budgetheadid)
         data = (balance_id,ownerid,plotid,indid,budgetid,100000,formatted_date)

        # Execute the query
         cur.execute(insert_query_balance, data)
         con.commit()     
    else:
       print(f"Found {result[0]}")
       namechange = 10000

       update_balance = """
                        UPDATE balance 
                        SET balance = balance + %s 
                        where balance_id = %s;"""
       data = (namechange,result[0])
       cur.execute(update_balance,data)
       print(update_balance)
       con.commit()


def update_balancedata_if_name_changed(ownerid,plotid,indid):
    cur, con = database_connect()
    cur.execute("use kpezdmc_version1")
    budgetid = get_budget_head("Name Change")
    print(f"Return ID {budgetid}")
    recorcheck = f"select balance_id from balance where industry_id = {indid} and budget_head_id = {budgetid};"
    cur.execute(recorcheck)
    result = cur.fetchone()
    print(f"Balance id {result}")
    if result is None:
         print("Not Found")
         print(f"owner id {ownerid} plot id {plotid} industry id {indid}")
         insert_query_balance = """INSERT INTO balance (balance_id,owner_id,plot_id,industry_id,budget_head_id,balance,update_at) 
                                    VALUES (%s,%s,%s,%s,%s,%s,%s)"""
        # Get plot id and owner id from tree
        # Cureent Date
         current_date = datetime.now()

        # Format the current date
         formatted_date = current_date.strftime("%Y/%m/%d %H:%M:%S")  # Example format: 2024-09-03
        # Data to be inserted
         balance_id = get_balance_id("balance","balance_id")
        # print(budgetheadid)
         data = (balance_id,ownerid,plotid,indid,budgetid,50000,formatted_date)

        # Execute the query
         cur.execute(insert_query_balance, data)
         con.commit()     
    else:
       print(f"Found {result[0]}")
       namechange = 50000
       update_balance = """
                        UPDATE balance 
                        SET balance = balance + %s 
                        where balance_id = %s;"""
       data = (50000,result[0])
       cur.execute(update_balance,(50000,result[0]))
       print(update_balance)
       print(result[0])
       con.commit()



def updatebudget(head,amount):
    cursor,connection = database_connect()
        # Specify the budget head (e.g., Maintenance, Bore Hole, AGR, etc.)
    budget_head_name = head.get()
    charges = float(amount.get())

    # Get the budget_head_id for the specified budget head
    cursor.execute("SELECT budget_head_id FROM budget_heads WHERE budget_head_name = %s", (budget_head_name,))
    budget_head_id = cursor.fetchone()
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
        balance = f"SELECT balance_id, balance FROM balance WHERE industry_id = {industryid} AND budget_head_id = {budget_head_id};"
        cursor.execute(balance)
    
        existing_balance = cursor.fetchone()
        print(industry)
        # Example logic for calculating the balance based on covered area (you can modify this logic)
        if budget_head_name == "AGR" or budget_head_name == "Maintenance" or budget_head_name == "Lease Money":
            new_balance = calculate_maintenance_price(coverd_area,charges)
        else:
            new_balance = charges
        # Get the current datetime
        now = datetime.now()

        if existing_balance:
            # Update the balance if the record exists
            balanceid, current_balance = existing_balance
            updatequery = """
                UPDATE balance 
                SET balance = balance + %s,update_at = %s 
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

def updatebudgetforsingle(head,amount,gplotid,gownerid,gindid):
    cursor,connection = database_connect()
        # Specify the budget head (e.g., Maintenance, Bore Hole, AGR, etc.)
    budget_head_name = head.get()
    charges = float(amount.get())

    # Get the budget_head_id for the specified budget head
    cursor.execute("SELECT budget_head_id FROM budget_heads WHERE budget_head_name = %s", (budget_head_name,))
    budget_head_id = cursor.fetchone()
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
    fetchall = f"select p.Area,o.ownname,i.ind_name,p.id,o.id,i.id from plots p join plot_ownership po on p.id = po.plot_id join ownertable o on o.id = po.owner_id left join industries i on i.plot_id = p.id where p.id = {gplotid} and o.id = {gownerid} and i.id = {gindid} and i.ind_name is not null order by i.created_at desc;"
    cursor.execute(fetchall)
    industries = cursor.fetchone()

    
    coverd_area,ownername,industryname,plotid,ownerid,industryid = industries
    #print(industry)
    # Check if the industry already has a balance entry for the specified budget head
    balance = f"SELECT balance_id, balance FROM balance WHERE industry_id = {industryid} AND budget_head_id = {budget_head_id};"
    cursor.execute(balance)

    existing_balance = cursor.fetchone()
    print(industries)
    # Example logic for calculating the balance based on covered area (you can modify this logic)
    if budget_head_name == "AGR" or budget_head_name == "Maintenance" or budget_head_name == "Lease Money":
        new_balance = calculate_maintenance_price(coverd_area,charges)
    else:
        new_balance = charges
    # Get the current datetime
    now = datetime.now()

    if existing_balance:
        # Update the balance if the record exists
        balanceid, current_balance = existing_balance
        updatequery = """
            UPDATE balance 
            SET balance = balance + %s,update_at = %s 
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


# image read function
def image_read(path):
    open_image = Image.open(path)
    image = ct.CTkImage(open_image)
    return image
def image_read_logo(path):
    open_image = Image.open(path)
    image = ct.CTkImage(open_image,size=(70,70))
    return image
    