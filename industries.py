import customtkinter as ct
import tkinter 
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry
import mysql.connector
from datetime import datetime
from mysql.connector import Error
import database as db
# Save record fn
def save_record(indnameentery,naturecombo,statuscombo,modecombo,areaentery,dateentery):
    if indnameentery.get() == "" or naturecombo.get() == "Select Nature" or statuscombo.get() == "Select Status" or modecombo.get() == "Select Mode" :
        messagebox.showerror("Error","All fileds are required")
    else:
        try:
            cur, con = db.database_connect()
            cur.execute("use kpezdmc_version1")
            plotid,owner_id = select_data()
            if plotid == '':
                messagebox.ERROR("Error","First select the plot from Tree")
            else:
                # Data Entery into Plot Table
                ind_id = db.get_id("industries") # Get Plot tabel Id auto incrment by 1
                # Define the SQL query to insert data
                insert_query = """INSERT INTO industries (id,ind_name,ind_nature,ind_status,ind_mode,coverd_area,plot_id,created_at) 
                                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""

                # Get plot id and owner id from tree
                # Cureent Date
                current_date = datetime.now()

                # Format the current date
                formatted_date = current_date.strftime("%Y/%m/%d %H:%M:%S")  # Example format: 2024-09-03
                print(plotid)
                # Data to be inserted
                data = (ind_id,indnameentery.get(),naturecombo.get(),statuscombo.get(),modecombo.get(),areaentery.get(),
                        plotid,formatted_date)

                # Execute the query
                cur.execute(insert_query, data)
        # End of entery to industry table

        # Entery to industry ownership table
                    # Data Entery into plot_ownership
                ownership_id = db.get_id("industry_ownerships") # Get plot_Ownership Id Auto increment by 1
                # Define the SQL query to insert data
                insert_query = """INSERT INTO industry_ownerships (id,industry_id,owner_id,start_date,i0_status,created_at) 
                                                        VALUES (%s, %s, %s,%s,%s,%s)"""

                # Cureent Date
                current_date = datetime.now()

                # Format the current date
                formatted_date = current_date.strftime("%Y/%m/%d %H:%M:%S")  # Example format: 2024-09-03
                
                # Data to be inserted
                data = (ownership_id,ind_id,owner_id,dateentery.get(),"Established",formatted_date)

                # Execute the query
                cur.execute(insert_query, data) 
                # Commit the transaction
                con.commit()
                clear_fields(indnameentery,naturecombo,statuscombo,modecombo,areaentery,dateentery)
                treeview_data()
        except Error as e:
                messagebox.showerror("Error",f"Database error : {e}")
        finally:
                if con.is_connected():
                    cur.close()
                    con.close()
                    print("MySQL connection is closed")
        treeview_data()

# Select Data from tree
def select_data():
    global treeview
    try:
        global plot_id,owner_id
        plot_id = ''
        owner_id = ''
        index = treeview.selection()
        content = treeview.item(index)
        row = content['values']
        plot_id = row[7]
        owner_id = row[8]
        print(f"Select Data : {row}")
        print(plot_id,owner_id)  # Print the values of the clicked row
        return plot_id,owner_id
    except:
        messagebox.showerror("Error","Select plot first")

#Search Record

def search_record(searchcombo,searchentry):
    global treeview
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
        query =f"select p.plot_number,p.zone,p.Area,o.ownname,o.Mobile,i.ind_name,i.ind_nature,p.id,o.id from plots p join plot_ownership po on p.id = po.plot_id join ownertable o on o.id = po.owner_id left join industries i on i.plot_id = p.id where {cond} like {value};"
        print(query)
        cur.execute(query)
        result = cur.fetchall()
        treeview.delete(*treeview.get_children())
        for record in result:
            treeview.insert('',ct.END,values=record)
        print(result)
 
# Clear Fields
def clear_fields(indnameentery,naturecombo,statuscombo,modecombo,areaentery,dateentery):
    indnameentery.delete(0,ct.END)
    naturecombo.set("Select Nature")
    statuscombo.set("Select Status")
    modecombo.set("Select Mode")
    areaentery.delete(0,ct.END)
    from datetime import date
    dateentery.set_date(date.today())


# Display data in treeview 
def treeview_data():
    cur, con = db.database_connect()
    cur.execute("use kpezdmc_version1")
    query = """select p.plot_number,p.zone,p.Area,o.ownname,o.Mobile,i.ind_name,i.ind_nature,p.id,o.id
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
                order by p.created_at desc;"""
    cur.execute(query)
    plot_record = cur.fetchall()
    treeview.delete(*treeview.get_children())
    treeview.tag_configure("highlight", background="lightyellow")
    for record in plot_record:
        treeview.insert('',ct.END,values=record)
def industries(app):
    global treeview
    fontlable = ("Poppins",14)
    fontlmenu = ("Poppins",18,"bold")
    fontentry = ("Poppins",10,"bold")
    fontbtn = ("Arial",16,"bold")
    indframe = ct.CTkFrame(app,width=900,height=600,fg_color="#17202a")
    indframe.place(x=158,y=82)
    backframe = ct.CTkFrame(indframe,fg_color="#17202a")
    backframe.place(x=0,y=0)
    industryframe = ct.CTkFrame(indframe,fg_color="#2c3e50",bg_color="#17202a",corner_radius=5,border_width=3,border_color="#85929e")
    industryframe.place(x=00,y=20)
    btnframe = ct.CTkFrame(indframe,fg_color="#17202a")
    btnframe.place(x=40,y=160)
    treeframe =ct.CTkFrame(indframe,fg_color="#2c3e50",bg_color="#17202a",corner_radius=5,border_width=3,border_color="#85929e")
    treeframe.place(x=0,y=250)
    photo_image = db.image_read(r"D:\Python\KPEZDMC\images\back.png")
    #tkinter.PhotoImage(file=r"D:\Python\KPEZDMC\images\back.png")
    homebtn = ct.CTkButton(backframe,image=photo_image,text="",font=fontbtn,width=30,hover_color="#1b4f72",fg_color="#17202a",bg_color="#17202a",
                            height=20,cursor="hand2",command=lambda:indframe.place_forget())
    homebtn.place(x=0,y=0)
    # Tree Frame start
    plotdetaillable = ct.CTkLabel(treeframe,text="Plot Details",font=("Arial",14,"bold"),
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
    cols = ("Plot #","Zone","Area","Owner","Mobile","indname","nature","Plot ID","Owner ID")
    vsb = ttk.Scrollbar(treeframe, orient="vertical")
    h_scroll = ttk.Scrollbar(indframe, orient="horizontal")
    treeview = ttk.Treeview(treeframe,columns = cols, show="headings",height=11,
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
    #treeview.bind("Button-1>",select_data)
    #treeview.bind('<<TreeviewSelect>>', lambda event: select_data(event='TreeviewSelect'))
    #db.database_connect()


    #End of Tree Frame ###########################################

    # Start of industry frame
    indinfolable = ct.CTkLabel(industryframe,text="Industry Information",font=("Arial",14,"bold"),
                            text_color="#f8f9f9",bg_color="#808b96",width=850,height=20)
    indinfolable.grid(row=0,column=0,columnspan=6,pady=(0,0))
    indnamelable = ct.CTkLabel(industryframe,text="Name ",font=fontlable,text_color="#f8f9f9")
    indnamelable.grid(row=1,column=0,padx=20,pady=12,sticky="w")

    indnameentery = ct.CTkEntry(industryframe,font=fontentry,width=180,
                                placeholder_text="Enter the Name",border_width=2,border_color="#17202a",
                                fg_color="#154360",text_color="White",placeholder_text_color="white")
    indnameentery.grid(row=1,column=1,padx=20)

    naturelable = ct.CTkLabel(industryframe,text="Zone",font=fontlable,text_color="#f8f9f9")
    naturelable.grid(row=1,column=2,padx=(0,0),pady=12,sticky="w")

    naturecombo = ct.CTkComboBox(industryframe,font=fontentry,width=180,
                                values=["Marble","Engineering","Grinding","Phrama"],border_width=2,border_color="#17202a",
                                fg_color="#154360",text_color="White",button_color="#17202a",button_hover_color="#2471a3")
    naturecombo.grid(row=1,column=3,padx=20)

    statuslable = ct.CTkLabel(industryframe,text="Status",font=fontlable,text_color="#f8f9f9")
    statuslable.grid(row=1,column=4,padx=0,pady=12,sticky="w")


    statuscombo = ct.CTkComboBox(industryframe,font=fontentry,width=180,
                                values=["Newly Alloted","Under Construction","Operational","Closed"],border_width=2,border_color="#17202a",
                                fg_color="#154360",text_color="White",button_color="#17202a",button_hover_color="#2471a3")
    statuscombo.grid(row=1,column=5)

    modelable = ct.CTkLabel(industryframe,text="Mode",font=fontlable,text_color="#f8f9f9")
    modelable.grid(row=2,column=0,padx=(20,0),pady=12,sticky="w")

    modecombo = ct.CTkComboBox(industryframe,font=fontentry,width=180,
                                values=["Manual","Automatic","Semi Automatic"],border_width=2,border_color="#17202a",
                                fg_color="#154360",text_color="White",button_color="#17202a",button_hover_color="#2471a3")
    modecombo.grid(row=2,column=1)

    arealable = ct.CTkLabel(industryframe,text="Area",font=fontlable,text_color="#f8f9f9")
    arealable.grid(row=2,column=2,padx=00,pady=12,sticky="w")

    areaentery = ct.CTkEntry(industryframe,font=fontentry,width=180,
                                placeholder_text="Coverd Area",border_width=2,border_color="#17202a",
                                fg_color="#154360",text_color="White",placeholder_text_color="white")
    areaentery.grid(row=2,column=3,padx=(0,0))

    datelable = ct.CTkLabel(industryframe,text="Date",font=fontlable,text_color="#f8f9f9")
    datelable.grid(row=2,column=4,padx=(0,7),pady=12,sticky="w")
    dateentery = DateEntry(industryframe,font=fontentry,width=22,height=12,date_pattern="yyyy/mm/dd",
                        background='darkblue', foreground='white', borderwidth=2)

    dateentery.grid(row=2,column=5,padx=(1,2))

    # End of Left Frame

    # Strat of button Frame
    
    savebtn = ct.CTkButton(btnframe,text="Save Record",width=150,
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

    searchlable = ct.CTkLabel(btnframe,text="Search By :",text_color="white")
    searchlable.grid(row=1,column=0,padx=(50,0),pady=15)

    searchcombo = ct.CTkComboBox(btnframe,font=fontentry,width=150,
                                values=["Plot Number","Owner Name","Industry Name"],text_color="white",fg_color="#2c3e50",button_color="#707b7c",button_hover_color="#2471a3")
    searchcombo.grid(row=1,column=1,padx=(30,0),pady=15)

    searchentry = ct.CTkEntry(btnframe,placeholder_text="Search By",width=150,border_width=2,border_color="#99a3a4",
                                fg_color="#2c3e50",text_color="White",placeholder_text_color="white")
    searchentry.grid(row=1,column=2,padx=(30,0),pady=15)

    searchbtn = ct.CTkButton(btnframe,text="Search",fg_color="#2c3e50",bg_color="#17202a",corner_radius=5,border_width=2,border_color="#85929e",width=150,command=lambda:search_record(searchcombo,searchentry))
    searchbtn.grid(row=1,column=3,padx=(30,0),pady=15)
