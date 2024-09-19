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
        print(head)
        return budget_head_id
    else:
        return result[0]