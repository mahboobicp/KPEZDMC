import customtkinter as ct
import tkinter 
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry
import mysql.connector
from datetime import datetime
from mysql.connector import Error
import database as db

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



def show_allRecord(tree):
    global selected_item_global
    tree.unbind("<<TreeviewSelect>>")
    
    # Clear the Treeview
    for row in tree.get_children():
        tree.delete(row)
    # Insert new data into the Treeview
    cur, con = db.database_connect()
    global treeview, treeflag
    treeflag = True
    cur.execute("use kpezdmc_version1")
    query = """select p.plot_number,p.zone,p.Area,o.ownname,i.ind_status,i.ind_name,i.ind_nature,p.id,o.id,i.id
                from plots p
                join
                plot_ownership po
                on p.id = po.plot_id
                join
                ownertable o
                on o.id = po.owner_id
                left join
                industries i
                on i.plot_id = p.id
                order by i.created_at desc;"""
    cur.execute(query)
    plot_record = cur.fetchall()
    #treeview.delete(*treeview.get_children())
    for record in plot_record:
        tree.insert('',ct.END,values=record)
    selected_item_global = None
    # Rebind the event after updating the Treeview
    tree.bind("<<TreeviewSelect>>", select_data)
    print("Treeview updated with new data.")


def select_data(event):
    global gownerid,gplotid,gindid,oldname,treeview,selected_item_global 
    row = []
    selected_item = treeview.selection()  # Get selected item
    if selected_item:
        selected_item_global = selected_item[0]  # Save the selection globally
        row = treeview.item(selected_item_global, "values")
        print(f"Selected: {row}")
        print(row)
        if row[7] is None:
            gplotid = 0
        else:
            gplotid = row[7]
        if row[8] == 'None':
            gownerid = 0
        else:
            gownerid = row[8]
        if row[9] == 'None':
            gindid = 0
        else:
            gindid = row[9]
    
    else:
        print("No row selected")
        selected_item_global = None  # Clear the global if no row is selected
    
  
    print(gplotid,gownerid,gindid)

   
    #update_balancedata_if_name_changed(gownerid,gplotid,gindid)
    # Print the values of the clicked row
