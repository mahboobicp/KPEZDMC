import customtkinter as ct
import tkinter 
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry
import mysql.connector
from datetime import datetime
from mysql.connector import Error
import database as db
#Search Record

def search_record(searchcombo,searchentry):
    cond=searchcombo.get()
    value=f"'%{searchentry.get()}%'"
    if value == '':
        messagebox.showerror("Error","Enter Value to Search")
    else:
        if cond == "Plot Number":
            cond = "p.plot_number"
        elif cond == "Name":
            cond = "o.ownname"
        elif cond == "CNIC":
            cond = "o.CNIC"
        cur,con = db.database_connect()
        cur.execute("use kpezdmc_version1")
        query =f"select p.plot_number,p.zone,p.Area,o.CNIC,o.ownname,o.Mobile,po.start_date from plots p join plot_ownership po on p.id = po.plot_id join ownertable o on o.id = po.owner_id where {cond} like {value};"
        print(query)
        cur.execute(query)
        result = cur.fetchall()
        treeview.delete(*treeview.get_children())
        for record in result:
            treeview.insert('',ct.END,values=record)
        print(result)
 
""" # Clear Fields
def clear_fields(indnameentery,naturecombo,
                locationentery,statuscombo,modecombo,areaentery,
                cnicentry,nameentry,mobileentery,emmailentery,
                addressentry,dateentery):
    indnameentery.delete(0,ct.END)
    naturecombo.set("NEZ")
    locationentery.delete(0,ct.END)
    statuscombo.set("Industerial")
    modecombo.set("Acquired")
    areaentery.delete(0,ct.END)
    cnicentry.delete(0,ct.END)
    nameentry.delete(0,ct.END)
    mobileentery.delete(0,ct.END)
    emmailentery.delete(0,ct.END)
    addressentry.delete(0,ct.END)
    from datetime import date
    dateentery.set_date(date.today())

 """
# Display data in treeview 
def treeview_data():
    cur, con = db.database_connect()
    cur.execute("use kpezdmc_version1")
    query = """select p.plot_number,p.zone,p.Area,o.CNIC,o.ownname,o.Mobile,po.start_date
                from plots p
                join
                plot_ownership po
                on p.id = po.plot_id
                join
                ownertable o
                on o.id = po.owner_id
                order by o.created_at desc;"""
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
    photo_image = tkinter.PhotoImage(file=r"D:\Python\KPEZDMC\images\back.png")
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
    cols = ("Plot #","Zone","Area","CNIC","Owner","Mobile","Date")
    treeview = ttk.Treeview(treeframe,columns = cols, show="headings",height=11,padding=1)

    treeview.column("Plot #", width=50)
    treeview.heading ('Plot #', text='Plot #',anchor="center")
    treeview.column("Area", width=70,anchor="center")
    treeview.heading ('Zone', text='Zone')
    treeview.column ('Zone',anchor="center")
    treeview.column("Area", width=80,anchor="center")
    treeview.heading ('Area', text="Area",anchor="center")
    treeview.column("CNIC", width=130,anchor="center")
    treeview.heading ('CNIC', text="CNIC",anchor="center")
    treeview.column("Owner", width=140,anchor="center")
    treeview.heading ('Owner', text='Owner Name')
    treeview.column("Mobile", width=100,anchor="center")
    treeview.heading ('Mobile', text="Mobile #")
    treeview.column("Date", width=130,anchor="center")
    treeview.heading ('Date', text="Allotment Date")
    treeview.pack(side="left")
    treeview_data()
    vsb = ttk.Scrollbar(treeframe, orient="vertical", command=treeview.yview)
    vsb.pack(side='right', fill='y')
    treeview.configure(yscrollcommand=vsb.set)
    #vsb.grid(row=0,column=1,pady=0)
    db.database_connect()


    #End of Tree Frame ###########################################
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
                                values=["Newly Alloted","Under Construction","Opertional","Closed"],border_width=2,border_color="#17202a",
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
                           fg_color="#2c3e50",bg_color="#17202a",corner_radius=5,border_width=2,border_color="#85929e")
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
                                values=["Plot Number","Name","CNIC"],text_color="white",fg_color="#2c3e50",button_color="#707b7c",button_hover_color="#2471a3")
    searchcombo.grid(row=1,column=1,padx=(30,0),pady=15)

    searchentry = ct.CTkEntry(btnframe,placeholder_text="Search By",width=150,border_width=2,border_color="#99a3a4",
                                fg_color="#2c3e50",text_color="White",placeholder_text_color="white")
    searchentry.grid(row=1,column=2,padx=(30,0),pady=15)

    searchbtn = ct.CTkButton(btnframe,text="Search",fg_color="#2c3e50",bg_color="#17202a",corner_radius=5,border_width=2,border_color="#85929e",width=150,command=lambda:search_record(searchcombo,searchentry))
    searchbtn.grid(row=1,column=3,padx=(30,0),pady=15)
