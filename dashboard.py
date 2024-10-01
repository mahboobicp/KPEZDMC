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
def dashboard(dashboard):
    global treeview
    fontlable = ("Poppins",14)
    fontlmenu = ("Poppins",18,"bold")
    fontentry = ("Poppins",10,"bold")
    fontbtn = ("Arial",16,"bold")
        
    fontlable = ("Open Sans",14)
    fontlmenu = ("Poppins",18,"bold")
    fontdash = ("Poppins",24,"bold")
    fontentry = ("Arial",10,"bold")
    fontbtn = ("Arial",16,"bold")
    dfonts = ("Poppins",40,"bold")
    fnt = ("Open Sans",14)
    dashboard = ct.CTkFrame(dashboard,width=900,height=600,fg_color="#17202a")
    dashboard.place(x=158,y=82)
    backframe = ct.CTkFrame(dashboard,fg_color="#17202a")
    backframe.place(x=0,y=0)
    plotdetailsframe = ct.CTkFrame(dashboard,width=200,height=250,fg_color="#7d6608",bg_color="#17202a")
    plotdetailsframe.place(x=30,y=30)
    industrydetailsframe = ct.CTkFrame(dashboard,width=200,height=250,fg_color="#2e4053",bg_color="#17202a",)
    industrydetailsframe.place(x=280,y=30)
    paymentdetailsframe = ct.CTkFrame(dashboard,width=200,height=250,fg_color="#6c3483",bg_color="#17202a")
    paymentdetailsframe.place(x=28,y=315)
    otherdetailsframe = ct.CTkFrame(dashboard,width=200,height=250,fg_color="#b9770e",bg_color="#17202a")
    otherdetailsframe.place(x=278,y=315)
    eventsframe = ct.CTkFrame(dashboard,width=290,height=540,fg_color="#78281f",bg_color="#17202a")
    eventsframe.place(x=530,y=30)
    plotnumber = tkinter.StringVar()
    # Plots Details
    cur,con=db.database_connect()
    cur.execute("select count(*) from plots;")
    plotnumber = cur.fetchone()
    totalplot = f"Total Plots : {plotnumber[0]}"
    dtotalplots = ct.CTkLabel(plotdetailsframe,text=totalplot,text_color="white",font=fnt)
    dtotalplots.place(x=50,y=110)
    indplot = tkinter.StringVar()
    cur.execute("select count(*) from plots where Land_Type = 'Industrial';")
    indplot = cur.fetchone()
    industrialplot = f"Industerial Plots : {indplot[0]}"
    dindustrialplot = ct.CTkLabel(plotdetailsframe,text=industrialplot,text_color="white",font=fnt)
    dindustrialplot.place(x=30,y=140)
    cur.execute("select count(*) from plots where Land_Type = 'Commercial';")
    complot = cur.fetchone()
    commercialplot = f"Commercial Plots : {complot[0]}"
    dcommercialplot = ct.CTkLabel(plotdetailsframe,text=commercialplot,text_color="white",font=fnt)
    dcommercialplot.place(x=30,y=170)
    cur.execute("select count(*) from plots where Land_Type = 'Other';")
    othplot = cur.fetchone()
    if othplot == "None":
        othplot = 00
    otherplot = f"Other Entity Plots : {othplot[0]}"
    otherplots = ct.CTkLabel(plotdetailsframe,text=otherplot,text_color="white",font=fnt)
    otherplots.place(x=30,y=200)
    plot_image = tkinter.PhotoImage(file=r"D:\Python\KPEZDMC\images\plotting.png")
    plotinfo = ct.CTkLabel(plotdetailsframe,image=plot_image,text="")
    plotinfo.pack()
    plottext = ct.CTkLabel(plotdetailsframe,text="Plots Detail",font=fontdash,text_color="white")
    plottext.pack(padx=35,pady=(0,160))
    
    ind_image = tkinter.PhotoImage(file=r"D:\Python\KPEZDMC\images\factory.png")
    indinfo = ct.CTkLabel(industrydetailsframe,image=ind_image,text="")
    indinfo.pack()
    indtext = ct.CTkLabel(industrydetailsframe,text="Industries Info",font=fontdash,text_color="white")
    indtext.pack(padx=25,pady=(0,160))
    # Industries Details
    cur,con=db.database_connect()
    cur.execute("select count(*) from industries;")
    number = cur.fetchone()
    totalindustry = f"Total Industries : {number[0]}"
    dtotalindustries = ct.CTkLabel(industrydetailsframe,text=totalindustry,text_color="white",font=fnt)
    dtotalindustries.place(x=40,y=110)
    operational = tkinter.StringVar()
    cur.execute("select count(*) from industries where ind_status = 'Operational';")
    operational = cur.fetchone()
    operationaltxt = f"Opertional Units : {operational[0]}"
    operationallbl = ct.CTkLabel(industrydetailsframe,text=operationaltxt,text_color="white",font=fnt)
    operationallbl.place(x=40,y=140)
    cur.execute("select count(*) from industries where ind_status = 'Under Construction';")
    underconstruction = cur.fetchone()
    underconstructiontxt = f"Under Construction Units : {underconstruction[0]}"
    underconstructionlbl = ct.CTkLabel(industrydetailsframe,text=underconstructiontxt,text_color="white",font=fnt)
    underconstructionlbl.place(x=10,y=170)
    cur.execute("select count(*) from industries where ind_status = 'Closed';")
    closed = cur.fetchone()
    closetxt = f"Close Units : {closed[0]}"
    closelbl = ct.CTkLabel(industrydetailsframe,text=closetxt,text_color="white",font=fnt)
    closelbl.place(x=65,y=200)
    # Start of Paymnets details 
    
    pay_image = tkinter.PhotoImage(file=r"D:\Python\KPEZDMC\images\payment.png")
    payinfo = ct.CTkLabel(paymentdetailsframe,image=pay_image,text="")
    payinfo.pack()
    paytext = ct.CTkLabel(paymentdetailsframe,text="Payment Info",font=fontdash,text_color="white")
    paytext.pack(padx=30,pady=(0,160))
    cash_image = tkinter.PhotoImage(file=r"D:\Python\KPEZDMC\images\money.png")
    # Start of Bore Hole
    queryforpayment = """
                    SELECT SUM(amount) 
                    FROM payments
                    WHERE budget_head_id = (SELECT budget_head_id FROM budget_heads WHERE budget_head_name = 'Bore Hole')
                    AND MONTH(payment_date) = MONTH(CURRENT_DATE())
                    AND YEAR(payment_date) = YEAR(CURRENT_DATE());
                    """
    cur.execute(queryforpayment)
    fetchamount = cur.fetchone()
    amounttext = f"-  Bore Hole : {fetchamount[0]}"
    amountlable = ct.CTkLabel(paymentdetailsframe,text=amounttext,text_color="white",font=("Arial",14))
    amountlable.place(x=25,y=125)
    # End of Bore Hole Calculation
    # Start of Maintanance calculation
    queryforpayment = """
                    SELECT SUM(amount) 
                    FROM payments
                    WHERE budget_head_id = (SELECT budget_head_id FROM budget_heads WHERE budget_head_name = 'Maintanance')
                    AND MONTH(payment_date) = MONTH(CURRENT_DATE())
                    AND YEAR(payment_date) = YEAR(CURRENT_DATE());
                    """
    cur.execute(queryforpayment)
    fetchamount = cur.fetchone()
    amounttext = f"-  Maintanance : {fetchamount[0]}"
    amountlable = ct.CTkLabel(paymentdetailsframe,text=amounttext,text_color="white",font=("Arial",14))
    amountlable.place(x=25,y=150)
    # End of Maintanance 
    # Start of AGR
    queryforpayment = """
                    SELECT SUM(amount) 
                    FROM payments
                    WHERE budget_head_id = (SELECT budget_head_id FROM budget_heads WHERE budget_head_name = 'AGR')
                    AND MONTH(payment_date) = MONTH(CURRENT_DATE())
                    AND YEAR(payment_date) = YEAR(CURRENT_DATE());
                    """
    cur.execute(queryforpayment)
    fetchamount = cur.fetchone()
    amounttext = f"-  AGR : {fetchamount[0]}"
    amountlable = ct.CTkLabel(paymentdetailsframe,text=amounttext,text_color="white",font=("Arial",14))
    amountlable.place(x=25,y=175)
    # End of AGR
    # Start of Land Price 
    queryforpayment = """
                    SELECT SUM(amount) 
                    FROM payments
                    WHERE budget_head_id = (SELECT budget_head_id FROM budget_heads WHERE budget_head_name = 'Land Price')
                    AND MONTH(payment_date) = MONTH(CURRENT_DATE())
                    AND YEAR(payment_date) = YEAR(CURRENT_DATE());
                    """
    cur.execute(queryforpayment)
    fetchamount = cur.fetchone()
    if fetchamount[0]:
        amounttext = f"-  Land Price : {float(fetchamount[0])/1000000} M"
    amountlable = ct.CTkLabel(paymentdetailsframe,text=amounttext,text_color="white",font=("Arial",14))
    amountlable.place(x=25,y=200)
    #end of Land Price
    recivables = ct.CTkLabel(paymentdetailsframe,image=cash_image,text="")
    recivables.place(x=25,y=100)
    recivablestext = ct.CTkLabel(paymentdetailsframe,text="Recivables",font=("Poppins",16,"bold"),text_color="white")
    recivablestext.place(x=60,y=102)
    
    # Start of Summary widget
    sum_image = tkinter.PhotoImage(file=r"D:\Python\KPEZDMC\images\summary.png")
    suminfo = ct.CTkLabel(otherdetailsframe,image=sum_image,text="")
    suminfo.pack()
    sumtext = ct.CTkLabel(otherdetailsframe,text="Summary",font=fontdash,text_color="white")
    sumtext.pack(padx=50,pady=(0,0))
    #Sumary calculation
    query = """select i.ind_name,b.budget_head_name,p.amount
                from payments p
                join 
                budget_heads b on
                b.budget_head_id = p.budget_head_id
                join industries i 
                on i.id = p.industry_id
                order by p.payment_date desc
                limit 2;"""

    cur.execute(query)
    result=cur.fetchall()
    for res in result:
        repo = f"{res[0]} Deposit \n Rs. {res[2]} in {res[1]}"
        eventlable =ct.CTkLabel(otherdetailsframe,text=repo,font=("Arial",14),text_color="white")
        linelabe =ct.CTkLabel(otherdetailsframe,text="~~~~~~~~~~~~~~~~~~~~~",text_color="white")
        linelabe.pack()
        eventlable.pack()

    linelabe =ct.CTkLabel(otherdetailsframe,text="~~~~~~~~~~~~~~~~~~~~~",text_color="white")
    linelabe.pack(pady=(0,10))
    #End Summary calculation
    
    logs_image = tkinter.PhotoImage(file=r"D:\Python\KPEZDMC\images\cloud.png")
    logsinfo = ct.CTkLabel(eventsframe,image=logs_image,text="")
    logsinfo.pack()
    logstext = ct.CTkLabel(eventsframe,text="Recent Activities",font=fontdash,text_color="white")
    logstext.pack(padx=60,pady=(0,0))
    #payment Events Start
    cur,con =db.database_connect()
    query = """
            select i.ind_name,a.changed_field,a.old_value,a.new_value 
            from industries_audit a
            join industries i
            on
            i.id = a.industry_id
            order 
            by a.changed_at desc
            limit 5;
            """

    cur.execute(query)
    result=cur.fetchall()
    for res in result:
        repo = f"Industry : {res[0]} \n {res[1]} Changed From \n {res[2]} To {res[3]}"
        eventlable =ct.CTkLabel(eventsframe,text=repo,font=("Arial",14),text_color="white")
        linelabe =ct.CTkLabel(eventsframe,text="~~~~~~~~~~~~~~~~~~~~~~~~~",text_color="white")
        linelabe.pack()
        eventlable.pack()

    linelabe =ct.CTkLabel(eventsframe,text="~~~~~~~~~~~~~~~~~~~~~~~~~",text_color="white")
    linelabe.pack(pady=(0,0))
    evetdetails = ct.CTkLabel(eventsframe,text="Details of Most Recent Activities",font=("Poppins",17,"bold"),
                            text_color="#025c64",bg_color="white",corner_radius=10)
    evetdetails.pack(pady=(0,10))
