import customtkinter as ct
import tkinter 
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry
import mysql.connector
from datetime import datetime
from mysql.connector import Error
import database as db
gplotid=None
gownerid=None
gindid=None

# Global variable to set selection

# Function for transfer of plot

def plot_transfer(cnicentry,nameentry,mobileentery,emmailentery,addressentry,dateentery):
    global gownerid,gplotid,gindid 
    try:
        cur,con = db.database_connect()
        cur.execute(f"Select id from ownertable where cnic = {cnicentry.get()};")
        confirm = messagebox.askyesno("Confirm Update", "Do you want to update the Record?")
        if confirm:
            result1 = cur.fetchone()
            print(f"resutl {result1}")
            if result1 is not None:
                ownerid = result1[0]
                print(gownerid,gplotid,gindid,ownerid)
            else:         
                # Data Entery into OWNERTABLE 
                ownerid = db.get_id("ownertable") # Get Owner Id Auto increment by 1
                # Define the SQL query to insert data
                insert_query = """INSERT INTO ownertable (id,cnic,ownname,mobile,email,address,created_at) 
                                                        VALUES (%s, %s, %s,%s,%s,%s,%s)"""

                # Cureent Date
                current_date = datetime.now()

                # Format the current date
                formatted_date = current_date.strftime("%Y/%m/%d %H:%M:%S")  # Example format: 2024-09-03
                
                # Data to be inserted
                data = (ownerid,cnicentry.get(),nameentry.get(),mobileentery.get(),emmailentery.get(),
                            addressentry.get(),formatted_date)

                # Execute the query
                cur.execute(insert_query, data) 
                con.commit()
            cur,con = db.database_connect()
            cur.execute(f"select id from plot_ownership where plot_id = {gplotid};")
            plotid = cur.fetchone()
            plotownershipid = plotid[0]
            print(plotownershipid)
            # Prepare update query
            update_query = """
            UPDATE plot_ownership
            SET  
                owner_id = %s, 
                start_date = %s,  
                po_status = %s, 
                updated_at = %s
            WHERE id = %s
            """
            print(dateentery.get())

            # Values to update
            update_values = (ownerid,dateentery.get(),'Treansferd',dateentery.get(),plotownershipid)

            # Execute the update
            cur.execute(update_query,update_values)

            # Commit the transaction
            con.commit()

            print(f"Record with ID {plotownershipid} updated successfully.")
            treeview_data()
        else:
            messagebox.INFO("Cancelled","Update cancelled by the user")
    except Error as e:
            messagebox.showerror("Error",f"Database error : {e}")
    finally:
            if con.is_connected():
                cur.close()
                con.close()
                print("MySQL connection is closed")


def investor_details(event,cnicentry,nameentry,mobileentery,emmailentery,addressentry):
    cur,con = db.database_connect()
    cur.execute(f"Select ownname,mobile,email,address from ownertable where cnic = {cnicentry.get()};")
    result = cur.fetchone()
    if result is not None:
        nameentry.delete(0, ct.END)  # Clear existing text
        nameentry.insert(0, result[0])  # Insert new text
        mobileentery.delete(0, ct.END)  # Clear existing text
        mobileentery.insert(0, result[1])  # Insert new text
        emmailentery.delete(0, ct.END)  # Clear existing text
        emmailentery.insert(0, result[2])  # Insert new text
        addressentry.delete(0, ct.END)  # Clear existing text
        addressentry.insert(0, result[3])  # Insert new text
    else:
       nameentry.delete(0, ct.END)  # Clear existing text 
       mobileentery.delete(0, ct.END)  # Clear existing text
       emmailentery.delete(0, ct.END)  # Clear existing text
       addressentry.delete(0, ct.END)  # Clear existing text

def show_allRecord(tree):
    global selected_item_global
    #tree.unbind("<<TreeviewSelect>>")
    
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
   
    # Rebind the e selected_item_global = Nonevent after updating the Treeview
    #tree.bind("<<TreeviewSelect>>", select_data)
    print("Treeview updated with new data.")
    
    
def clear_treeview(tree):
    for row in tree.get_children():
        tree.delete(row)

# Function to unbind all events from the Treeview


# Select Data from tree
def select_data(event):
    global gownerid,gplotid,gindid,oldname,treeview,selected_item_global 
    row = []
    selected_item = treeview.selection()  # Get selected item
    if selected_item:
        selected_item_global = selected_item[0]  # Save the selection globally
        row = treeview.item(selected_item[0], "values")
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
          # Clear the global if no row is selected
    
  
    print(gplotid,gownerid,gindid)

    
    #update_balancedata_if_name_changed(gownerid,gplotid,gindid)
    # Print the values of the clicked row

#Search Record
# Function for Search Record
def search_record(searchcombo,searchentry):
    cond=searchcombo.get()
    value=f"'%{searchentry.get()}%'"
    if value == '':
        messagebox.showerror("Error","Enter Value to Search")
    else:
        if cond == "Plot Number":
            cond = "p.plot_number"
        elif cond == "Owner Name":
            cond = "o.ownname"
        elif cond == "Industry Name":
            cond = "i.ind_name"
        cur,con = db.database_connect()
        cur.execute("use kpezdmc_version1")
        query =f"select p.plot_number,p.zone,p.Area,o.ownname,o.Mobile,i.ind_name,i.ind_nature,p.id,o.id,i.id from plots p join plot_ownership po on p.id = po.plot_id join ownertable o on o.id = po.owner_id left join industries i on i.plot_id = p.id where {cond} like {value};"
        #print(query)
        cur.execute(query)
        result = cur.fetchall()
        treeview.delete(*treeview.get_children())
        for record in result:
            treeview.insert('',ct.END,values=record)
        plotid = result[0][7]
        indid  = result[0][8]
        ownid = result[0][9]
# Clear Fields
def clear_fields(paymentgeadcombo,amountentery,dateentery):
    paymentgeadcombo.set("Select Head")
    amountentery.delete(0,ct.END)
    from datetime import date
    dateentery.set_date(date.today())


# Display data in treeview 
def treeview_data():
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
    treeview.delete(*treeview.get_children())
    treeview.tag_configure("highlight", background="lightyellow")
    for record in plot_record:
        treeview.insert('',ct.END,values=record)
def transfer(app):
    gplotid = None
    gownerid = None
    gindid = None
    global treeview,baltreeview,paytreeview,oldname,oldstatus,newstatus,newstatuscombo,oldnature
    fontlable = ("Poppins",14)
    fontlmenu = ("Poppins",18,"bold")
    fontentry = ("Poppins",10,"bold")
    fontbtn = ("Arial",16,"bold")
    reansferframe = ct.CTkFrame(app,width=900,height=600,fg_color="#17202a")
    reansferframe.place(x=158,y=82)
    backframe = ct.CTkFrame(reansferframe,fg_color="#17202a")
    backframe.place(x=0,y=0)
    btnframe = ct.CTkFrame(reansferframe,fg_color="#17202a")
    btnframe.place(x=40,y=5)
    treeframe =ct.CTkFrame(reansferframe,fg_color="#2c3e50",bg_color="#17202a",corner_radius=5,border_width=3,border_color="#85929e")
    treeframe.place(x=0,y=60)
    ownerframe = ct.CTkFrame(reansferframe,fg_color="#2c3e50",bg_color="#17202a",corner_radius=5,border_width=2,border_color="#04747e")
    ownerframe.place(x=0,y=330)
    transferbtn = ct.CTkButton(reansferframe,text="Transfer",fg_color="#2c3e50",bg_color="#17202a",corner_radius=5,font=("Arial",20,'bold'),
                              border_width=2,border_color="#85929e",width=200,height=60,command=lambda:plot_transfer(cnicentry,nameentry,mobileentery,emmailentery,addressentry,dateentery))
    transferbtn.place(x=300,y=480)
    photo_image = db.image_read(r"D:\Python\KPEZDMC\images\back.png")
    #tkinter.PhotoImage(file=r"D:\Python\KPEZDMC\images\back.png")
    homebtn = ct.CTkButton(backframe,image=photo_image,text="",font=("Arial",20,'bold'),width=30,hover_color="#1b4f72",fg_color="#17202a",bg_color="#17202a",
                            height=20,cursor="hand2",command=lambda:reansferframe.place_forget())
    homebtn.place(x=0,y=0)
    # Tree Frame start
    plotdetaillable = ct.CTkLabel(treeframe,text="Plot / Industry Details",font=("Arial",14,"bold"),
                            text_color="#f8f9f9",bg_color="#808b96",width=850,height=20)
    plotdetaillable.pack()
    style = ttk.Style()
    # Configure Treeview heading (the column headers)
    style.configure("Treeview.Heading",
                font=("Helvetica", 11),       # Font and size of the headings
                background="black",           # Background color of the heading
                foreground="black",           # Text color of the heading
                fieldbackground="2c3e50",
                relief="raised",                  # Border style of the heading (flat, raised, sunken, etc.)
                anchor="center")   
    # Configure Treeview styles
    style.configure("Treeview",
                    background="#2c3e50",    # Background color of the cells
                    foreground="white",        # Text color
                    fieldbackground="2c3e50",   # Background color of the field
                    rowheight=25)              # Row height

    # Configure selected row colors
    style.map("Treeview",
            background=[('selected', '#2980b9')],  # Background color when row is selected
            foreground=[('selected', 'white')]) # Text color when row is selected
    cols = ("Plot #","Zone","Area","Owner","Status","indname","nature","Plot ID","Owner ID","Indid")
    vsb = ttk.Scrollbar(treeframe, orient="vertical")
    h_scroll = ttk.Scrollbar(reansferframe, orient="horizontal")
    treeview = ttk.Treeview(treeframe,columns = cols, show="headings",height=8,
                            yscrollcommand=vsb.set,xscrollcommand=h_scroll.set)

    treeview.column("Plot #", width=50,stretch=False)
    treeview.heading ('Plot #', text='Plot #',anchor="center")
    treeview.column("Area", width=80,anchor="center",stretch=False)
    treeview.heading ('Zone', text='Zone')
    treeview.column ('Zone',anchor="center",stretch=False)
    treeview.column("Area", width=80,anchor="center",stretch=False)
    treeview.heading ('Area', text="Area",anchor="center")
    treeview.column("Owner", width=140,anchor="center",stretch=False)
    treeview.heading ('Owner', text='Owner Name')
    treeview.column("Status", width=120,anchor="center",stretch=False)
    treeview.heading ('Status', text="Status")
    treeview.column("indname", width=130,anchor="center",stretch=False)
    treeview.heading ('indname', text="Industry Name",anchor="center")
    treeview.column("nature", width=110,anchor="center",stretch=False)
    treeview.heading ('nature', text="Nature",anchor="center")
    treeview.column("Plot ID", width=0,anchor="center",stretch=False)
    treeview.heading ('Plot ID', text="Plot ID")
    treeview.column("Owner ID", width=0,anchor="center",stretch=False)
    treeview.heading ('Owner ID', text="Owner ID")
    treeview.column("Indid", width=0,anchor="center",stretch=False)
    treeview.heading ('Indid', text="Indid")
    treeview_data()
    treeview.configure(yscrollcommand=vsb.set)
    # Add the horizontal scrollbar
    treeview.configure(xscrollcommand=h_scroll.set)
    vsb.config(command=treeview.yview)
    h_scroll.config(command=treeview.xview)
    # Pack the treeview and scrollbar
    treeview.pack(side=tkinter.LEFT)
    #h_scroll.pack(side=tkinter.BOTTOM, fill=tkinter.X)
    vsb.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    #vsb.grid(row=0,column=1,pady=0)
    #h_scroll.place(x=4,y=495,width=840)
    #treeview.bind("Button-1>",select_data(event='TreeviewSelect'))
    treeview.bind('<<TreeviewSelect>>', select_data)
    #db.database_connect()

     #End of Tree Frame ###########################################
    
    # Strat of button Frame
    searchlable = ct.CTkLabel(btnframe,text="Search By :",text_color="white")
    searchlable.grid(row=0,column=0,padx=(2,0),pady=15)

    searchcombo = ct.CTkComboBox(btnframe,font=fontentry,width=150,
                                values=["Plot Number","Owner Name","Industry Name"],text_color="white",fg_color="#2c3e50",button_color="#707b7c",button_hover_color="#2471a3")
    searchcombo.grid(row=0,column=1,padx=(30,0),pady=15)

    searchentry = ct.CTkEntry(btnframe,placeholder_text="Search By",width=150,border_width=2,border_color="#99a3a4",
                                fg_color="#2c3e50",text_color="White",placeholder_text_color="white")
    searchentry.grid(row=0,column=2,padx=(30,0),pady=15)

    searchbtn = ct.CTkButton(btnframe,text="Search",fg_color="#2c3e50",bg_color="#17202a",corner_radius=5,border_width=2,border_color="#85929e",width=150,command=lambda:search_record(searchcombo,searchentry))
    searchbtn.grid(row=0,column=3,padx=(30,0),pady=15)
    showallbtn = ct.CTkButton(btnframe,text="Show All",fg_color="#2c3e50",bg_color="#17202a",corner_radius=5,
                              border_width=2,border_color="#85929e",width=150,command=lambda:show_allRecord(treeview))
    showallbtn.grid(row=0,column=4,padx=(30,0),pady=15)
    
    # Start of Owner Frame


    plotdetails = ct.CTkLabel(ownerframe,text="Investor Information",font=("Arial",14,"bold"),
                            text_color="#f8f9f9",bg_color="#04747e",width=850,height=20)
    plotdetails.grid(row=0,column=0,columnspan=6)



    cniclable = ct.CTkLabel(ownerframe,text="CNIC #",font=fontlable,text_color="#f8f9f9")
    cniclable.grid(row=1,column=0,padx=20,pady=13,sticky="w")

    cnicentry = ct.CTkEntry(ownerframe,font=fontentry,width=180,
                                placeholder_text="Enter the CNIC",border_width=2,border_color="#17202a",
                                fg_color="#154360",text_color="White",placeholder_text_color="white")
    cnicentry.grid(row=1,column=1,padx=(33,20))


    namelable = ct.CTkLabel(ownerframe,text="Name ",font=fontlable,text_color="#f8f9f9")
    namelable.grid(row=1,column=2,padx=0,pady=12,sticky="w")

    nameentry = ct.CTkEntry(ownerframe,font=fontentry,width=180,
                                placeholder_text="Enter the Name",border_width=2,border_color="#17202a",
                                fg_color="#154360",text_color="White",placeholder_text_color="white")
    nameentry.grid(row=1,column=3)


    mobilelable = ct.CTkLabel(ownerframe,text="Mobile",font=fontlable,text_color="#f8f9f9")
    mobilelable.grid(row=1,column=4,padx=(30,7),pady=12,sticky="w")

    mobileentery = ct.CTkEntry(ownerframe,font=fontentry,width=180,
                                placeholder_text="Enter Mobile Number",border_width=2,border_color="#17202a",
                                fg_color="#154360",text_color="White",placeholder_text_color="white")
    mobileentery.grid(row=1,column=5,padx=(15,2))


    emaillable = ct.CTkLabel(ownerframe,text="Email",font=fontlable,text_color="#f8f9f9")
    emaillable.grid(row=4,column=0,padx=20,pady=12,sticky="w")
    emmailentery = ct.CTkEntry(ownerframe,font=fontentry,width=180,
                                placeholder_text="Enter Mobile Number",border_width=2,border_color="#17202a",
                                fg_color="#154360",text_color="White",placeholder_text_color="white")

    emmailentery.grid(row=4,column=1,padx=(33,20))

    addresslable = ct.CTkLabel(ownerframe,text="Address   ",font=fontlable,text_color="#f8f9f9")
    addresslable.grid(row=4,column=2,padx=(0,10),pady=12,sticky="w")
    addressentry = ct.CTkEntry(ownerframe,font=fontentry,width=180,
                                placeholder_text="Enter Mobile Address",border_width=2,border_color="#17202a",
                                fg_color="#154360",text_color="White",placeholder_text_color="white")

    addressentry.grid(row=4,column=3)

    datelable = ct.CTkLabel(ownerframe,text="Date",font=fontlable,text_color="#f8f9f9")
    datelable.grid(row=4,column=4,padx=(30,7),pady=12,sticky="w")
    dateentery = DateEntry(ownerframe,font=fontentry,width=22,height=12,date_pattern="yyyy/mm/dd",
                        background='darkblue', foreground='white', borderwidth=2)

    dateentery.grid(row=4,column=5,padx=(15,2))
    cnicentry.bind("<FocusOut>", lambda event:investor_details(event,cnicentry,nameentry,mobileentery,emmailentery,addressentry))
    # End of right Frame

    