import customtkinter as ct
import tkinter 
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
    recorcheck = f"select balance_id from balance where owner_id = {ownerid} and plot_id = {plotid} and industry_id = {indid} and budget_head_id = {budgetid};"
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
         data = (balance_id,ownerid,plotid,indid,budgetid,10000,formatted_date)

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
    recorcheck = f"select balance_id from balance where owner_id = {ownerid} and plot_id = {plotid} and industry_id = {indid} and budget_head_id = {budgetid};"
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