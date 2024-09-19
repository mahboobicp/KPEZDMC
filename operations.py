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

# Function to update Balance tree
def update_balancedata(gownerid,gplotid,gindid):
    cur, con = db.database_connect()
    cur.execute("use kpezdmc_version1")
    query = f"select b.budget_head_name,bb.balance,bb.update_at from balance bb join budget_heads b on b.budget_head_id = bb.budget_head_id where bb.plot_id={gplotid} or bb.owner_id={gownerid} or bb.industry_id = {gindid} order by bb.update_at desc;"
    cur.execute(query)
    bal_record = cur.fetchall()
    baltreeview.delete(*baltreeview.get_children())
    for record in bal_record:
        baltreeview.insert('',ct.END,values=record)
#Update Nature
def updated_nature(newnaturecombo):
    if newnaturecombo.get() == "Select Nature":
        messagebox.showerror("Error","Please First Select Nature")
    else:
        try:
            cur, con = db.database_connect()
            cur.execute("use kpezdmc_version1")
            if gindid is None:
                messagebox.showerror("Error","First select the Industry from above tree")
            else:
                # Update industries table
                current_date = datetime.now()

                # Format the current date
                formatted_date = current_date.strftime("%Y/%m/%d %H:%M:%S")
                update_query = f"update industries set ind_nature = '{newnaturecombo.get()}', updated_at = '{formatted_date}' where id = {gindid};"
                # Define the SQL query to insert data
                print(update_query)
                print(gplotid,gindid,gownerid)
                # Execute the query
                cur.execute(update_query)
                con.commit()
              
                #clear_fields(newnameentery)
        except Error as e:
                messagebox.showerror("Error",f"Database error : {e}")
        finally:
                if con.is_connected():
                    cur.close()
                    con.close()
                    print("MySQL connection is closed")

#Update Status
def updated_status(newstatuscombo):
    if newstatuscombo.get() == "Select Status":
        messagebox.showerror("Error","Please First Select Status")
    else:
        try:
            cur, con = db.database_connect()
            cur.execute("use kpezdmc_version1")
            if gindid is None:
                messagebox.showerror("Error","First select the Industry from above tree")
            else:
                # Update industries table
                current_date = datetime.now()

                # Format the current date
                formatted_date = current_date.strftime("%Y/%m/%d %H:%M:%S")
                update_query = f"update industries set ind_Status = '{newstatuscombo.get()}', updated_at = '{formatted_date}' where id = {gindid};"
                # Define the SQL query to insert data
                print(update_query)
                print(gplotid,gindid,gownerid)
                # Execute the query
                cur.execute(update_query)
                con.commit()
              
                #clear_fields(newnameentery)
                
        except Error as e:
                messagebox.showerror("Error",f"Database error : {e}")
        finally:
                if con.is_connected():
                    cur.close()
                    con.close()
                    print("MySQL connection is closed")

#Update Name
def update_name(newnameentery):
    if newnameentery.get() == "":
        messagebox.showerror("Error","Please Enter The New Name")
    else:
        try:
            cur, con = db.database_connect()
            cur.execute("use kpezdmc_version1")
            if gindid is None:
                messagebox.showerror("Error","First select the Industry from above tree")
            else:
                # Update industries table
                current_date = datetime.now()

                # Format the current date
                formatted_date = current_date.strftime("%Y/%m/%d %H:%M:%S")
                update_query = f"update industries set ind_name = '{newnameentery.get()}', updated_at = '{formatted_date}' where id = {gindid};"
                # Define the SQL query to insert data
                print(update_query)
                print(gplotid,gindid,gownerid)
                # Execute the query
                cur.execute(update_query)
                con.commit()
              
                #clear_fields(newnameentery)
                
        except Error as e:
                messagebox.showerror("Error",f"Database error : {e}")
        finally:
                if con.is_connected():
                    cur.close()
                    con.close()
                    print("MySQL connection is closed")

        # End of entery to industry table

# Select Data from tree
def select_data(event):
    global gownerid,gplotid,gindid,oldname
    row = []
    index = treeview.selection()
    print(f"Index is {index}")
    content = treeview.item(index)
    row = content['values']
    print(row)
    if row[7] == 'None':
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
    print(gplotid,gownerid,gindid)
    oldname.set(f"Industry Name Is : {row[5]}")
    oldstatus.set(f"Current Status Is : {row[4]}")
    oldnature.set(f"Current Nature Is : {row[6]}")
    update_balancedata(gownerid,gplotid,gindid)
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
        query =f"select p.plot_number,p.zone,p.Area,o.ownname,o.Mobile,i.ind_name,i.ind_nature,p.id,i.id,o.id from plots p join plot_ownership po on p.id = po.plot_id join ownertable o on o.id = po.owner_id left join industries i on i.plot_id = p.id where {cond} like {value};"
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
    cur, con = db.database_connect()
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
def operations(app):
    gplotid = None
    gownerid = None
    gindid = None
    global treeview,baltreeview,paytreeview,oldname,oldstatus,newstatus,newstatuscombo,oldnature
    fontlable = ("Poppins",14)
    fontlmenu = ("Poppins",18,"bold")
    fontentry = ("Poppins",10,"bold")
    fontbtn = ("Arial",16,"bold")
    operationframe = ct.CTkFrame(app,width=900,height=600,fg_color="#17202a")
    operationframe.place(x=158,y=82)
    backframe = ct.CTkFrame(operationframe,fg_color="#17202a")
    backframe.place(x=0,y=0)
    btnframe = ct.CTkFrame(operationframe,fg_color="#17202a")
    btnframe.place(x=40,y=5)
    treeframe =ct.CTkFrame(operationframe,fg_color="#2c3e50",bg_color="#17202a",corner_radius=5,border_width=3,border_color="#85929e")
    treeframe.place(x=0,y=60)
    tabsframe =ct.CTkFrame(operationframe,fg_color="#2c3e50",bg_color="#17202a",corner_radius=5,border_width=3,border_color="#85929e")
    tabsframe.place(x=5,y=320)
    balanceframe = ct.CTkFrame(operationframe,fg_color="#2c3e50",bg_color="#17202a",corner_radius=5,border_width=3,border_color="#85929e")
    balanceframe.place(x=430,y=320)
    photo_image = tkinter.PhotoImage(file=r"D:\Python\KPEZDMC\images\back.png")
    homebtn = ct.CTkButton(backframe,image=photo_image,text="",font=fontbtn,width=30,hover_color="#1b4f72",fg_color="#17202a",bg_color="#17202a",
                            height=20,cursor="hand2",command=lambda:operationframe.place_forget())
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
    h_scroll = ttk.Scrollbar(operationframe, orient="horizontal")
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
    treeview.bind('<<TreeviewSelect>>', lambda event: select_data(event='TreeviewSelect'))
    #db.database_connect()

     #End of Tree Frame ###########################################
    # Start of Balance Tree
    balancelable = ct.CTkLabel(balanceframe,text="Balance Summary",font=("Arial",14,"bold"),
                            text_color="#f8f9f9",bg_color="#808b96",width=420,height=25)
    balancelable.pack(side=tkinter.TOP,pady=(2,0))
    balcols = ("bhn","Balance","Date")
    balvs = ttk.Scrollbar(balanceframe, orient="vertical")
    baltreeview = ttk.Treeview(balanceframe,columns = balcols, show="headings",height=8)
    baltreeview.pack(side=tkinter.LEFT,padx=(4,0),pady=(0,4))
    baltreeview.column("bhn", width=170,stretch=False)
    baltreeview.heading ('bhn', text='Payment Head',anchor="center")
    baltreeview.column("Balance", width=110,anchor="center",stretch=False)
    baltreeview.heading ('Balance', text='Balance')
    baltreeview.column ('Date',anchor="center",stretch=False,width=120)
    baltreeview.heading ('Date', text="Date",anchor="center")
    

    baltreeview.configure(yscrollcommand=balvs.set)
    # Add the horizontal scrollbar
    balvs.config(command=baltreeview.yview)
    # Pack the baltreeview and scrollbar
    #h_scroll.pack(side=tkinter.BOTTOM, fill=tkinter.X)
    balvs.pack(side=tkinter.RIGHT, fill=tkinter.Y,pady=(1,5),padx=(0,4))
   
 
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
                              border_width=2,border_color="#85929e",width=150,command=lambda:treeview_data())
    showallbtn.grid(row=0,column=4,padx=(30,0),pady=15)
    # Start of Tabs Frame
    # Create a CTkTabView
    tab_view = ct.CTkTabview(tabsframe,fg_color="#2c3e50",bg_color="#17202a",text_color="white")
    tab_view.pack(expand=False, padx=4, pady=(2,4))
   # tab_view.place(x=10,y=20)
    # Add tabs to the TabView
    tab_view.add("Name Change")
    tab_view.add("Status Change")
    tab_view.add("Nature Change")
    tab_view.add("NOC For WAPDA")

    # Set default active tab (optional)
    tab_view.set("Name Change")
    # Add content to Name Change
    label1 = ct.CTkLabel(tab_view.tab("Name Change"),text="Change of Name ", font=("Helvetica", 24,"bold"),text_color="white")
    label1.place(x=110,y=2)
    oldname = tkinter.StringVar()
    oldname.set("Industry Name : ")
    oldnamelable = ct.CTkLabel(tab_view.tab("Name Change"),textvariable=oldname,font=("Helvetica", 18),text_color="white")
    oldnamelable.place(x=20,y=40)
    newnamelable = ct.CTkLabel(tab_view.tab("Name Change"),text="Enter name     :   ",font=("Helvetica", 18),text_color="white")
    newnamelable.place(x=20,y=80)
    newname = tkinter.StringVar()
    newnameentery = ct.CTkEntry(tab_view.tab("Name Change"),font=("Helvetica", 18),width=200,
                                placeholder_text="Enter New Name",border_width=2,border_color="#17202a",
                                fg_color="#154360",text_color="White",placeholder_text_color="white",textvariable=newname)
    newnameentery.place(x=160,y=80)
    newnameconflable = ct.CTkLabel(tab_view.tab("Name Change"),text="New Name Will be : ",font=("Helvetica", 18),text_color="white")
    newnameconflable.place(x=20,y=120)
    newnameconfirm = ct.CTkLabel(tab_view.tab("Name Change"),textvariable=newname,font=("Helvetica", 18,"bold"),text_color="white")
    newnameconfirm.place(x=180,y=120)
    savebtn = ct.CTkButton(tab_view.tab("Name Change"),text="Update Record",width=200,height=30,hover_color="darkgreen",cursor="hand2",
                           fg_color="green",bg_color="#2c3e50",corner_radius=10,border_width=2,border_color="#17202a",
                           command=lambda:update_name(newnameentery))
    savebtn.place(x=110,y=160)
   

    # Add content to Status Change
    label1 = ct.CTkLabel(tab_view.tab("Status Change"),text="Change of Name ", font=("Helvetica", 24,"bold"),text_color="white")
    label1.place(x=110,y=2)
    oldstatus = tkinter.StringVar()
    oldstatus.set("Current Status : ")
    oldstatuslable = ct.CTkLabel(tab_view.tab("Status Change"),textvariable=oldstatus,font=("Helvetica", 18),text_color="white")
    oldstatuslable.place(x=20,y=40)
    newstatuslable = ct.CTkLabel(tab_view.tab("Status Change"),text="Update Status     :   ",font=("Helvetica", 18),text_color="white")
    newstatuslable.place(x=20,y=80)
    newstatus=tkinter.StringVar()
    newstatuscombo = ct.CTkComboBox(tab_view.tab("Status Change"),font=fontentry,width=180,
                                values=["Select Status","Under Construction","Operational","Closed",],border_width=2,border_color="#17202a",
                                fg_color="#154360",text_color="White",button_color="#17202a",button_hover_color="#2471a3")
    newstatuscombo.place(x=160,y=80)

    
    savebtn = ct.CTkButton(tab_view.tab("Status Change"),text="Update Record",width=200,height=30,hover_color="darkgreen",cursor="hand2",
                           fg_color="green",bg_color="#2c3e50",corner_radius=10,border_width=2,border_color="#17202a",
                           command=lambda:updated_status(newstatuscombo))
    savebtn.place(x=110,y=160)
     # Add content to Nature Change
    label1 = ct.CTkLabel(tab_view.tab("Nature Change"),text="Change of Nature ", font=("Helvetica", 24,"bold"),text_color="white")
    label1.place(x=110,y=2)
    oldnature = tkinter.StringVar()
    oldnature.set("Current Status : ")
    oldnaturelable = ct.CTkLabel(tab_view.tab("Nature Change"),textvariable=oldnature,font=("Helvetica", 18),text_color="white")
    oldnaturelable.place(x=20,y=40)
    newnaturelable = ct.CTkLabel(tab_view.tab("Nature Change"),text="Update Nature     :   ",font=("Helvetica", 18),text_color="white")
    newnaturelable.place(x=20,y=80)
    newnaturecombo = ct.CTkComboBox(tab_view.tab("Nature Change"),font=fontentry,width=180,
                                values=["Select Nature","Marble","Pharma","Engineering",],border_width=2,border_color="#17202a",
                                fg_color="#154360",text_color="White",button_color="#17202a",button_hover_color="#2471a3")
    newnaturecombo.place(x=160,y=80)

    
    savebtn = ct.CTkButton(tab_view.tab("Nature Change"),text="Update Record",width=200,height=30,hover_color="darkgreen",cursor="hand2",
                           fg_color="green",bg_color="#2c3e50",corner_radius=10,border_width=2,border_color="#17202a",
                           command=lambda:updated_nature(newnaturecombo))
    savebtn.place(x=110,y=160)


