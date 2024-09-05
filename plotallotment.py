import customtkinter as ct
import tkinter 
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry
import mysql.connector
from datetime import datetime
from mysql.connector import Error
import database as db
# Clear Fields
def clear_fields(plotnumberentery,zonecombo,
                locationentery,landtypecombo,plotstatuscombo,areaentery,
                cnicentry,nameentry,mobileentery,emmailentery,
                addressentry,dateentery):
    plotnumberentery.delete(0,ct.END)
    zonecombo.set("NEZ")
    locationentery.delete(0,ct.END)
    landtypecombo.set("Industerial")
    plotstatuscombo.set("Acquired")
    areaentery.delete(0,ct.END)
    cnicentry.delete(0,ct.END)
    nameentry.delete(0,ct.END)
    mobileentery.delete(0,ct.END)
    emmailentery.delete(0,ct.END)
    addressentry.delete(0,ct.END)
    from datetime import date
    dateentery.set_date(date.today())


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
def save_record(plotnumberentery,zonecombo,
                locationentery,landtypecombo,plotstatuscombo,areaentery,
                cnicentry,nameentry,mobileentery,emmailentery,
                addressentry,dateentery):
    
    if plotnumberentery.get() == "" or areaentery.get() == "" or cnicentry.get() == "" or nameentry.get() == "" :
        messagebox.showerror("Error","All fileds are required")
    else:
        try:
            cur, con = db.database_connect()
            cur.execute("use kpezdmc_version1")
            
            # Data Entery into Plot Table
            plotid = db.get_id("plots") # Get Plot tabel Id auto incrment by 1
            # Define the SQL query to insert data
            insert_query = """INSERT INTO plots (id,plot_number,zone,location,plot_status,land_type,area,created_at) 
                                VALUES (%s, %s, %s,%s,%s,%s,%s,%s)"""

            # Cureent Date
            current_date = datetime.now()

            # Format the current date
            formatted_date = current_date.strftime("%Y/%m/%d %H:%M:%S")  # Example format: 2024-09-03
            
            # Data to be inserted
            data = (plotid,plotnumberentery.get(),zonecombo.get(),
                        locationentery.get(),landtypecombo.get(),plotstatuscombo.get(),areaentery.get(),formatted_date)

            # Execute the query
            cur.execute(insert_query, data)
        
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

            # Data Entery into plot_ownership
            po_ownerid = db.get_id("plot_ownership") # Get plot_Ownership Id Auto increment by 1
            # Define the SQL query to insert data
            insert_query = """INSERT INTO plot_ownership (id,plot_id,owner_id,start_date,po_status,created_at) 
                                                    VALUES (%s, %s, %s,%s,%s,%s)"""

            # Cureent Date
            current_date = datetime.now()

            # Format the current date
            formatted_date = current_date.strftime("%Y/%m/%d %H:%M:%S")  # Example format: 2024-09-03
            
            # Data to be inserted
            data = (po_ownerid,plotid,ownerid,dateentery.get(),"Alloted",formatted_date)

            # Execute the query
            cur.execute(insert_query, data) 
            # Commit the transaction
            con.commit()
            clear_fields(plotnumberentery,zonecombo,
                    locationentery,landtypecombo,plotstatuscombo,areaentery,
                    cnicentry,nameentry,mobileentery,emmailentery,
                    addressentry,dateentery)
        except Error as e:
            messagebox.showerror("Error",f"Database error : {e}")
        finally:
            if con.is_connected():
                cur.close()
                con.close()
                print("MySQL connection is closed")
        treeview_data()

def pltallotment(app):
    global treeview
    fontlable = ("Poppins",14)
    fontlmenu = ("Poppins",18,"bold")
    fontentry = ("Poppins",10,"bold")
    fontbtn = ("Arial",16,"bold")
    pltframe = ct.CTkFrame(app,width=900,height=600,fg_color="white")
    pltframe.place(x=158,y=82)
    backframe = ct.CTkFrame(pltframe,fg_color="white")
    backframe.place(x=0,y=0)
    photo_image = tkinter.PhotoImage(file=r"D:\Python\KPEZDMC\back.png")
    homebtn = ct.CTkButton(backframe,image=photo_image,text="",font=fontbtn,width=30,hover_color="white",fg_color="white",bg_color="white",
                            height=20,cursor="hand2",command=lambda:pltframe.place_forget())
    homebtn.pack(side="left")
    plotframe = ct.CTkFrame(pltframe,fg_color="#2c3e50",bg_color="white",corner_radius=5,border_width=3,border_color="#196f3d")
    #plotframe.grid(row=1,column=0)
    plotframe.place(x=0,y=28)
    ownerframe = ct.CTkFrame(pltframe,fg_color="#2c3e50",bg_color="white",corner_radius=5,border_width=3,border_color="#196f3d")
    ownerframe.place(x=0,y=155)
    btnframe = ct.CTkFrame(pltframe,fg_color="white")
    btnframe.place(x=40,y=285)
    treeframe =ct.CTkFrame(pltframe,fg_color="darkblue")
    treeframe.place(x=0,y=320)
    # Plot details Frame

    plotdetails = ct.CTkLabel(plotframe,text="Enter Plot Details",font=("Arial",14,"bold"),
                            text_color="#f8f9f9",bg_color="Green",width=850,height=20)
    plotdetails.grid(row=0,column=0,columnspan=6)
    plotnumberlable = ct.CTkLabel(plotframe,text="Plot #  ",font=fontlable,text_color="#f8f9f9")
    plotnumberlable.grid(row=1,column=0,padx=20,pady=12,sticky="w")

    plotnumberentery = ct.CTkEntry(plotframe,font=fontentry,width=180,
                                placeholder_text="Enter the Number",border_width=2,border_color="#27ae60",
                                fg_color="#abebc6")
    plotnumberentery.grid(row=1,column=1,padx=20)

    zonelable = ct.CTkLabel(plotframe,text="Zone",font=fontlable,text_color="#f8f9f9")
    zonelable.grid(row=1,column=2,padx=(0,0),pady=12,sticky="w")

    zonecombo = ct.CTkComboBox(plotframe,font=fontentry,width=180,
                                values=["Nowshera Econoic Zone","Nowshera Econoic Zone Ext."],border_width=2,border_color="#27ae60",
                                fg_color="#abebc6")
    zonecombo.grid(row=1,column=3,padx=20)

    locationlable = ct.CTkLabel(plotframe,text="Location",font=fontlable,text_color="#f8f9f9")
    locationlable.grid(row=1,column=4,padx=0,pady=12,sticky="w")

    locationentery = ct.CTkEntry(plotframe,font=fontentry,width=180,
                                placeholder_text="Enter Location",border_width=2,border_color="#27ae60",
                                fg_color="#abebc6")
    locationentery.grid(row=1,column=5,padx=(0,0))




    landtypelable = ct.CTkLabel(plotframe,text="Type",font=fontlable,text_color="#f8f9f9")
    landtypelable.grid(row=2,column=0,padx=20,pady=12,sticky="w")

    landtypecombo = ct.CTkComboBox(plotframe,font=fontentry,width=180,
                                values=["Industrial","Commercial"],border_width=2,border_color="#27ae60",
                                fg_color="#abebc6")
    landtypecombo.grid(row=2,column=1)

    plotstatuslable = ct.CTkLabel(plotframe,text="Status",font=fontlable,text_color="#f8f9f9")
    plotstatuslable.grid(row=2,column=2,padx=(0,0),pady=12,sticky="w")

    plotstatuscombo = ct.CTkComboBox(plotframe,font=fontentry,width=180,
                                values=["Acquired","Available"],border_width=2,border_color="#27ae60",
                                fg_color="#abebc6")
    plotstatuscombo.grid(row=2,column=3)

    arealable = ct.CTkLabel(plotframe,text="Area",font=fontlable,text_color="#f8f9f9")
    arealable.grid(row=2,column=4,padx=00,pady=12,sticky="w")

    areaentery = ct.CTkEntry(plotframe,font=fontentry,width=180,
                                placeholder_text="Enter Area in Acre",border_width=2,border_color="#27ae60",
                                fg_color="#abebc6")
    areaentery.grid(row=2,column=5,padx=(0,0))



    # End of Left Frame

    #################################################################################

    # Start of Owner Frame


    plotdetails = ct.CTkLabel(ownerframe,text="Investor Information",font=("Arial",14,"bold"),
                            text_color="#f8f9f9",bg_color="Green",width=850,height=20)
    plotdetails.grid(row=0,column=0,columnspan=6)



    cniclable = ct.CTkLabel(ownerframe,text="CNIC #",font=fontlable,text_color="#f8f9f9")
    cniclable.grid(row=1,column=0,padx=20,pady=13,sticky="w")

    cnicentry = ct.CTkEntry(ownerframe,font=fontentry,width=180,
                                placeholder_text="Enter the CNIC",border_width=2,border_color="#27ae60",
                                fg_color="#abebc6")
    cnicentry.grid(row=1,column=1,padx=(33,20))


    namelable = ct.CTkLabel(ownerframe,text="Name ",font=fontlable,text_color="#f8f9f9")
    namelable.grid(row=1,column=2,padx=0,pady=12,sticky="w")

    nameentry = ct.CTkEntry(ownerframe,font=fontentry,width=180,
                                placeholder_text="Enter the Name",border_width=2,border_color="#27ae60",
                                fg_color="#abebc6")
    nameentry.grid(row=1,column=3)


    mobilelable = ct.CTkLabel(ownerframe,text="Mobile",font=fontlable,text_color="#f8f9f9")
    mobilelable.grid(row=1,column=4,padx=(30,7),pady=12,sticky="w")

    mobileentery = ct.CTkEntry(ownerframe,font=fontentry,width=180,
                                placeholder_text="Enter Mobile Number",border_width=2,border_color="#27ae60",
                                fg_color="#abebc6")
    mobileentery.grid(row=1,column=5,padx=(15,2))


    emaillable = ct.CTkLabel(ownerframe,text="Email",font=fontlable,text_color="#f8f9f9")
    emaillable.grid(row=4,column=0,padx=20,pady=12,sticky="w")
    emmailentery = ct.CTkEntry(ownerframe,font=fontentry,width=180,
                                placeholder_text="Enter Mobile Number",border_width=2,border_color="#27ae60",
                                fg_color="#abebc6")

    emmailentery.grid(row=4,column=1,padx=(33,20))

    addresslable = ct.CTkLabel(ownerframe,text="Address   ",font=fontlable,text_color="#f8f9f9")
    addresslable.grid(row=4,column=2,padx=(0,10),pady=12,sticky="w")
    addressentry = ct.CTkEntry(ownerframe,font=fontentry,width=180,
                                placeholder_text="Enter Mobile Address",border_width=2,border_color="#27ae60",
                                fg_color="#abebc6")

    addressentry.grid(row=4,column=3)

    datelable = ct.CTkLabel(ownerframe,text="Date",font=fontlable,text_color="#f8f9f9")
    datelable.grid(row=4,column=4,padx=(30,7),pady=12,sticky="w")
    dateentery = DateEntry(ownerframe,font=fontentry,width=22,height=12,date_pattern="yyyy/mm/dd",
                        background='green', foreground='white', borderwidth=2)

    dateentery.grid(row=4,column=5,padx=(15,2))
    # End of right Frame

    # Strat of button Frame
    
    savebtn = ct.CTkButton(btnframe,text="Save Record",width=100,
                           command=lambda:save_record(plotnumberentery,zonecombo,
                                                     locationentery,landtypecombo,plotstatuscombo,areaentery,
                                                     cnicentry,nameentry,mobileentery,emmailentery,
                                                     addressentry,dateentery))
    savebtn.grid(row=0,column=0)

    showbtn = ct.CTkButton(btnframe,text="Show All",width=100,command=lambda:treeview_data())
    showbtn.grid(row=0,column=1,padx=10)

    searchlable = ct.CTkLabel(btnframe,text="Search By :")
    searchlable.grid(row=0,column=2)

    searchcombo = ct.CTkComboBox(btnframe,font=fontentry,width=180,
                                values=["Plot #","Name","CNIC"])
    searchcombo.grid(row=0,column=3)

    searchentry = ct.CTkEntry(btnframe,placeholder_text="Search By",width=150)
    searchentry.grid(row=0,column=4,padx=10)

    searchbtn = ct.CTkButton(btnframe,text="Search",width=100)
    searchbtn.grid(row=0,column=5,padx=10)

    ## Start of treeview
    
    cols = ("Plot #","Zone","Area","CNIC","Owner","Mobile","Date")
    treeview = ttk.Treeview(treeframe,columns = cols, show="headings",height=11)

    treeview.column("Plot #", width=60)
    treeview.heading ('Plot #', text='Plot #',anchor="center")
    treeview.column("Area", width=80,anchor="center")
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
    treeview.grid(row=0,column=0)
    #treeview.pack()
    treeview_data()
    vsb = ttk.Scrollbar(treeframe, orient="vertical", command=treeview.yview)
    #vsb.pack(side='right', fill='y')
    treeview.configure(yscrollcommand=vsb.set)
    vsb.grid(row=0,column=1,pady=0)
    db.database_connect()