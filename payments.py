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
# Save record fn
def save_record(paymentgeadcombo,amountentery,dateentery):
    
    if paymentgeadcombo.get() == "" or amountentery.get() == "":
        messagebox.showerror("Error","All fileds are required")
    else:
        try:
            cur, con = db.database_connect()
            cur.execute("use kpezdmc_version1")
            if gindid == '':
                messagebox.showerror("Error","First select the plot from Tree")
            else:
                # Data Entery into Plot Table
                pay_id = db.get_id("payments") # Get payment tabel Id auto incrment by 1
                # Define the SQL query to insert data
                print(gplotid,gindid,gownerid)
                insert_query = """INSERT INTO payments (id,owner_id,plot_id,industry_id,budget_head_id,amount,payment_date,created_at) 
                                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""

                # Get plot id and owner id from tree
                # Cureent Date
                current_date = datetime.now()

                # Format the current date
                formatted_date = current_date.strftime("%Y/%m/%d %H:%M:%S")  # Example format: 2024-09-03
                print(f"global Data{gplotid}")
                # Data to be inserted
                budgetheadid = db.get_budget_head(paymentgeadcombo.get())
               # print(budgetheadid)
                data = (pay_id,gownerid,gplotid,gindid,budgetheadid,amountentery.get(),dateentery.get(),formatted_date)

                # Execute the query
                cur.execute(insert_query, data)
                con.commit()
                clear_fields(paymentgeadcombo,amountentery,dateentery)
                update_balancedata(gownerid,gplotid,gindid)
                update_paymentdata(gownerid,gplotid,gindid)
        # End of entery to industry table

        except Error as e:
                messagebox.showerror("Error",f"Database error : {e}")
        finally:
                if con.is_connected():
                    cur.close()
                    con.close()
                    print("MySQL connection is closed")
        

# Select Data from tree
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

    update_paymentdata(gownerid,gplotid,gindid)
    update_balancedata(gownerid,gplotid,gindid)
    # Print the values of the clicked row

#Search Record
# Function to update payment tree
def update_paymentdata(gownerid,gplotid,gindid):
    global paytreeview,baltreeview,treeview
    cur, con = db.database_connect()
    cur.execute("use kpezdmc_version1")
    query = f"select b.budget_head_name,p.amount,p.payment_date from payments p join budget_heads b on b.budget_head_id = p.budget_head_id where p.plot_id={gplotid} and p.owner_id={gownerid} or p.industry_id = {gindid} order by p.payment_date desc;"
    cur.execute(query)
    pay_record = cur.fetchall()
    paytreeview.delete(*paytreeview.get_children())
    for record in pay_record:
        paytreeview.insert('',ct.END,values=record)
        
# Function to update Balance tree
def update_balancedata(gownerid,gplotid,gindid):
    global baltreeview,treeview,paytreeview
    cur, con = db.database_connect()
    cur.execute("use kpezdmc_version1")
    query = f"select b.budget_head_name,bb.balance,bb.update_at from balance bb join budget_heads b on b.budget_head_id = bb.budget_head_id where bb.plot_id={gplotid} and bb.owner_id={gownerid} or bb.industry_id = {gindid} order by bb.update_at desc;"
    cur.execute(query)
    bal_record = cur.fetchall()
    baltreeview.delete(*baltreeview.get_children())
    for record in bal_record:
        baltreeview.insert('',ct.END,values=record)
# Function for Search Record
def search_record(searchcombo,searchentry):
    global baltreeview,paytreeview,treeview
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
        print(result)
        #print(plotid,indid,ownid)
        #return plotid,indid,ownid
        #plot_id,owner_id,indid=select_data()
        #print(plot_id,owner_id,indid)
# Clear Fields
def clear_fields(paymentgeadcombo,amountentery,dateentery):
    paymentgeadcombo.set("Select Head")
    amountentery.delete(0,ct.END)
    from datetime import date
    dateentery.set_date(date.today())


# Display data in treeview 
def treeview_data():
    global baltreeview,paytreeview,treeview
    cur, con = db.database_connect()
    cur.execute("use kpezdmc_version1")
    query = """select p.plot_number,p.zone,p.Area,o.ownname,o.Mobile,i.ind_name,i.ind_nature,p.id,o.id,i.id
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
def payments(app):
    gplotid = None
    gownerid = None
    gindid = None
    global treeview,baltreeview,paytreeview
    fontlable = ("Poppins",14)
    fontlmenu = ("Poppins",18,"bold")
    fontentry = ("Poppins",10,"bold")
    fontbtn = ("Arial",16,"bold")
    indframe = ct.CTkFrame(app,width=900,height=600,fg_color="#17202a")
    indframe.place(x=158,y=82)
    backframe = ct.CTkFrame(indframe,fg_color="#17202a")
    backframe.place(x=0,y=0)
    paymentsframe = ct.CTkFrame(indframe,fg_color="#2c3e50",bg_color="#17202a",corner_radius=5,border_width=3,border_color="#85929e")
    paymentsframe.place(x=00,y=240)
    balanceframe = ct.CTkFrame(indframe,fg_color="#2c3e50",bg_color="#17202a",corner_radius=5,border_width=3,border_color="#85929e")
    balanceframe.place(x=440,y=370)
    btnframe = ct.CTkFrame(indframe,fg_color="#17202a")
    btnframe.place(x=40,y=5)
    treeframe =ct.CTkFrame(indframe,fg_color="#2c3e50",bg_color="#17202a",corner_radius=5,border_width=3,border_color="#85929e")
    treeframe.place(x=0,y=60)
    sumaryframe =ct.CTkFrame(indframe,fg_color="#2c3e50",bg_color="#17202a",corner_radius=5,border_width=3,border_color="#85929e")
    sumaryframe.place(x=0,y=370)
    photo_image = tkinter.PhotoImage(file=r"D:\Python\KPEZDMC\images\back.png")
    homebtn = ct.CTkButton(backframe,image=photo_image,text="",font=fontbtn,width=30,hover_color="#1b4f72",fg_color="#17202a",bg_color="#17202a",
                            height=20,cursor="hand2",command=lambda:indframe.place_forget())
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
    cols = ("Plot #","Zone","Area","Owner","Mobile","indname","nature","Plot ID","Owner ID","Indid")
    vsb = ttk.Scrollbar(treeframe, orient="vertical")
    h_scroll = ttk.Scrollbar(indframe, orient="horizontal")
    treeview = ttk.Treeview(treeframe,columns = cols, show="headings",height=5,
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
    treeview.column("Mobile", width=120,anchor="center",stretch=False)
    treeview.heading ('Mobile', text="Mobile #")
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
    treeview.bind('<<TreeviewSelect>>', lambda event: select_data(event='TreeviewSelect'))
    #db.database_connect()


    #End of Tree Frame ###########################################

    # Start of industry frame
    indinfolable = ct.CTkLabel(paymentsframe,text="Industry Information",font=("Arial",14,"bold"),
                            text_color="#f8f9f9",bg_color="#808b96",width=850,height=20)
    indinfolable.grid(row=0,column=0,columnspan=6,pady=(0,0))
    

    paymentheadlable = ct.CTkLabel(paymentsframe,text="Payment Head",font=fontlable,text_color="#f8f9f9")
    paymentheadlable.grid(row=1,column=0,padx=(20,0),pady=12,sticky="w")
    # code to get budget heads from table
    pcur,pcon = db.database_connect()
    # Query to get budget heads
    query = "SELECT budget_head_name FROM budget_heads"  # Replace with your table and column names
    pcur.execute(query) 
    # Fetch all the results from the executed query
    results = pcur.fetchall()
    # Extract the budget heads from the results and return them as a list
    budget_heads1 = [row[0] for row in results]
    paymentgeadcombo = ct.CTkComboBox(paymentsframe,font=fontentry,width=180,
                                values=budget_heads1,border_width=2,border_color="#17202a",
                                fg_color="#154360",text_color="White",button_color="#17202a",button_hover_color="#2471a3")
    paymentgeadcombo.grid(row=1,column=1)

    amountlabel = ct.CTkLabel(paymentsframe,text="Amount",font=fontlable,text_color="#f8f9f9")
    amountlabel.grid(row=1,column=2,padx=0,pady=12,sticky="w")

    amountentery = ct.CTkEntry(paymentsframe,font=fontentry,width=180,
                                placeholder_text="Amount in Rs.",border_width=2,border_color="#17202a",
                                fg_color="#154360",text_color="White",placeholder_text_color="white")
    amountentery.grid(row=1,column=3,padx=(0,0))

    datelable = ct.CTkLabel(paymentsframe,text="Payment Date",font=fontlable,text_color="#f8f9f9")
    datelable.grid(row=2,column=0,padx=(20,0),pady=12,sticky="w")
    dateentery = DateEntry(paymentsframe,font=fontentry,width=22,height=12,date_pattern="yyyy/mm/dd",
                        background='darkblue', foreground='white', borderwidth=2)
    dateentery.grid(row=2,column=1,padx=(1,2))

    savebtn = ct.CTkButton(paymentsframe,text="Save Record",width=180,
                           fg_color="#154360",corner_radius=5,border_width=2,border_color="#17202a",command=lambda:save_record(paymentgeadcombo,amountentery,dateentery))
    savebtn.grid(row=2,column=3,padx=(0,0))

    # End of Left Frame

    # Strat of button Frame
    
    """ savebtn = ct.CTkButton(btnframe,text="Save Record",width=150,
                           fg_color="#2c3e50",bg_color="#17202a",corner_radius=5,border_width=2,border_color="#85929e",
                           command=lambda:save_record(indnameentery,naturecombo,statuscombo,modecombo,areaentery,dateentery))
    savebtn.grid(row=0,column=0,padx=(40,0))
    updatebtn = ct.CTkButton(btnframe,text="Update Record",width=150,
                           fg_color="#2c3e50",bg_color="#17202a",corner_radius=5,border_width=2,border_color="#85929e")
    updatebtn.grid(row=0,column=1,padx=(30,0))

    showbtn = ct.CTkButton(btnframe,text="Show All",width=150,fg_color="#2c3e50",bg_color="#17202a",corner_radius=5,border_width=2,border_color="#85929e",command=lambda:treeview_data())
    showbtn.grid(row=0,column=2,padx=(30,0))

    clearbtn = ct.CTkButton(btnframe,text="Show All",width=150,fg_color="#2c3e50",bg_color="#17202a",corner_radius=5,border_width=2,border_color="#85929e",command=lambda:treeview_data())
    clearbtn.grid(row=0,column=3,padx=(30,0))
 """
    searchlable = ct.CTkLabel(btnframe,text="Search By :",text_color="white")
    searchlable.grid(row=0,column=0,padx=(50,0),pady=15)

    searchcombo = ct.CTkComboBox(btnframe,font=fontentry,width=150,
                                values=["Plot Number","Owner Name","Industry Name"],text_color="white",fg_color="#2c3e50",button_color="#707b7c",button_hover_color="#2471a3")
    searchcombo.grid(row=0,column=1,padx=(30,0),pady=15)

    searchentry = ct.CTkEntry(btnframe,placeholder_text="Search By",width=150,border_width=2,border_color="#99a3a4",
                                fg_color="#2c3e50",text_color="White",placeholder_text_color="white")
    searchentry.grid(row=0,column=2,padx=(30,0),pady=15)

    searchbtn = ct.CTkButton(btnframe,text="Search",fg_color="#2c3e50",bg_color="#17202a",corner_radius=5,border_width=2,border_color="#85929e",width=150,command=lambda:search_record(searchcombo,searchentry))
    searchbtn.grid(row=0,column=3,padx=(30,0),pady=15)

    # Payment Summary Tree Start
    # Configure selected row colors
    paymentlable = ct.CTkLabel(sumaryframe,text="Payments Summary",font=("Arial",14,"bold"),
                            text_color="#f8f9f9",bg_color="#808b96",width=410,height=22)
    paymentlable.pack(side=tkinter.TOP)
    style.map("Treeview",
            background=[('selected', '#2980b9')],  # Background color when row is selected
            foreground=[('selected', 'white')]) # Text color when row is selected
    cols = ("bhn","amount","Date")
    vsb = ttk.Scrollbar(sumaryframe, orient="vertical")
    paytreeview = ttk.Treeview(sumaryframe,columns = cols, show="headings",height=6)
    paytreeview.pack(side=tkinter.LEFT,padx=(4,0),pady=(0,4))
    paytreeview.column("bhn", width=170,stretch=False)
    paytreeview.heading ('bhn', text='Payment Head',anchor="center")
    paytreeview.column("amount", width=100,anchor="center",stretch=False)
    paytreeview.heading ('amount', text='Amount')
    paytreeview.column ('Date',anchor="center",stretch=False,width=120)
    paytreeview.heading ('Date', text="Date",anchor="center")
    

    paytreeview.configure(yscrollcommand=vsb.set)
    # Add the horizontal scrollbar
    vsb.config(command=paytreeview.yview)
    # Pack the paytreeview and scrollbar
    #h_scroll.pack(side=tkinter.BOTTOM, fill=tkinter.X)
    vsb.pack(side=tkinter.RIGHT, fill=tkinter.Y,padx=(0,2),pady=(1,4))

    # End of payment Tree

    # Start of Balance Tree
    balancelable = ct.CTkLabel(balanceframe,text="Balance Summary",font=("Arial",14,"bold"),
                            text_color="#f8f9f9",bg_color="#808b96",width=410,height=22)
    balancelable.pack(side=tkinter.TOP)
    balcols = ("bhn","Balance","Date")
    balvs = ttk.Scrollbar(balanceframe, orient="vertical")
    baltreeview = ttk.Treeview(balanceframe,columns = balcols, show="headings",height=6)
    baltreeview.pack(side=tkinter.LEFT,padx=(4,0),pady=(0,4))
    baltreeview.column("bhn", width=170,stretch=False)
    baltreeview.heading ('bhn', text='Payment Head',anchor="center")
    baltreeview.column("Balance", width=90,anchor="center",stretch=False)
    baltreeview.heading ('Balance', text='Balance')
    baltreeview.column ('Date',anchor="center",stretch=False,width=120)
    baltreeview.heading ('Date', text="Date",anchor="center")
    

    baltreeview.configure(yscrollcommand=balvs.set)
    # Add the horizontal scrollbar
    balvs.config(command=baltreeview.yview)
    # Pack the baltreeview and scrollbar
    #h_scroll.pack(side=tkinter.BOTTOM, fill=tkinter.X)
    balvs.pack(side=tkinter.RIGHT, fill=tkinter.Y,padx=(0,4),pady=(0,4))
   
   
