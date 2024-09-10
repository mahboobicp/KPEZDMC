import customtkinter as ct
import tkinter
from tkinter import ttk
from plotallotment import pltallotment 
from industries import industries
from payments import payments
import database as db

fontlable = ("Poppins",14)
fontlmenu = ("Poppins",18,"bold")
fontdash = ("Poppins",24,"bold")
fontentry = ("Arial",10,"bold")
fontbtn = ("Arial",16,"bold")
dfonts = ("Poppins",40,"bold")
fnt = ("Poppins",16)
app =ct.CTk()
app.geometry("1020x662+200+5")
app.resizable(0,0)
app.config(background="#17202a")
app.title("KPEZDMC IMS")
logo_image = tkinter.PhotoImage(file=r"D:\Python\KPEZDMC\images\industry.png")
headings = ct.CTkLabel(app,width=1180,image=logo_image,compound="left",height=60,text=" KPEZDMC Industries Information System",
                       font=("Poppins",28,"bold"),text_color="#f8f9f9",fg_color="#283747",anchor="w")

headings.grid(row=0,column=0,columnspan=5,sticky="w")

titlebar = ct.CTkLabel(app,width=1180,height=20,text="WELCOME : Mahboob \t\t\t Time = 12 : 12 : 00",
                       font=("Arial",14,"bold"),text_color="#f8f9f9",fg_color="#5d6d7e")
titlebar.grid(row=1,column=0,columnspan=3,sticky="s")
menuframe = ct.CTkFrame(app,fg_color="#212f3c",bg_color="#212f3c",corner_radius=200,width=200,height=362)
menuframe.place(x=1,y=82)
plotdetailsframe = ct.CTkFrame(app,width=200,height=250,fg_color="#7d6608",bg_color="#17202a")
plotdetailsframe.place(x=200,y=110)
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
industrydetailsframe = ct.CTkFrame(app,width=200,height=250,fg_color="#2e4053",bg_color="#17202a",)
industrydetailsframe.place(x=450,y=110)
ind_image = tkinter.PhotoImage(file=r"D:\Python\KPEZDMC\images\factory.png")
indinfo = ct.CTkLabel(industrydetailsframe,image=ind_image,text="")
indinfo.pack()
indtext = ct.CTkLabel(industrydetailsframe,text="Industries Info",font=fontdash,text_color="white")
indtext.pack(padx=25,pady=(0,160))
paymentdetailsframe = ct.CTkFrame(app,width=200,height=250,fg_color="#6c3483",bg_color="#17202a")
paymentdetailsframe.place(x=200,y=400)
pay_image = tkinter.PhotoImage(file=r"D:\Python\KPEZDMC\images\payment.png")
payinfo = ct.CTkLabel(paymentdetailsframe,image=pay_image,text="")
payinfo.pack()
paytext = ct.CTkLabel(paymentdetailsframe,text="Payment Info",font=fontdash,text_color="white")
paytext.pack(padx=30,pady=(0,160))
otherdetailsframe = ct.CTkFrame(app,width=200,height=250,fg_color="#b9770e",bg_color="#17202a")
otherdetailsframe.place(x=450,y=400)
sum_image = tkinter.PhotoImage(file=r"D:\Python\KPEZDMC\images\summary.png")
suminfo = ct.CTkLabel(otherdetailsframe,image=sum_image,text="")
suminfo.pack()
sumtext = ct.CTkLabel(otherdetailsframe,text="Summary",font=fontdash,text_color="white")
sumtext.pack(padx=50,pady=(0,160))
eventsframe = ct.CTkFrame(app,width=290,height=540,fg_color="#78281f",bg_color="#17202a")
eventsframe.place(x=700,y=110)
logs_image = tkinter.PhotoImage(file=r"D:\Python\KPEZDMC\images\cloud.png")
logsinfo = ct.CTkLabel(eventsframe,image=logs_image,text="")
logsinfo.pack()
logstext = ct.CTkLabel(eventsframe,text="Recent Activities",font=fontdash,text_color="white")
logstext.pack(padx=60,pady=(0,450))

# Start of menu Frame


photo_image = tkinter.PhotoImage(file=r"D:\Python\KPEZDMC\images\logo.png")
alt_image = tkinter.PhotoImage(file=r"D:\Python\KPEZDMC\images\alt.png")
factory_image = tkinter.PhotoImage(file=r"D:\Python\KPEZDMC\images\factory1.png")
owner_image = tkinter.PhotoImage(file=r"D:\Python\KPEZDMC\images\owner.png")
report_image = tkinter.PhotoImage(file=r"D:\Python\KPEZDMC\images\report.png")
payment_image = tkinter.PhotoImage(file=r"D:\Python\KPEZDMC\images\payment1.png")
transfer_image = tkinter.PhotoImage(file=r"D:\Python\KPEZDMC\images\transfer.png")
switch_image = tkinter.PhotoImage(file=r"D:\Python\KPEZDMC\images\switch.png")
split_image = tkinter.PhotoImage(file=r"D:\Python\KPEZDMC\images\split.png")
logimage =ct.CTkLabel(menuframe,image=photo_image,width=40,height=40,text="",anchor="e")
logimage.pack(padx=(20,20),pady=(20,60))
menulable = ct.CTkLabel(menuframe,text="Menu",font=fontlmenu,text_color="#f8f9f9",
                        bg_color="Green",width=150,height=40)
menulable.pack()

allotmentbtn = ct.CTkButton(menuframe,image=alt_image,text="Allotment",border_width=2,fg_color="#154360",border_color="#707b7c",font=fontbtn,width=150,
                            height=40,cursor="hand2",command=lambda:pltallotment(app))
allotmentbtn.pack(padx=3,pady=5)
industrybtn = ct.CTkButton(menuframe,image=factory_image,border_width=2,fg_color="#154360",border_color="#707b7c",
                           text="Industries",cursor="hand2",font=fontbtn,width=150,height=40,command=lambda:industries(app))
industrybtn.pack()
ownerbtn = ct.CTkButton(menuframe,image=owner_image,border_width=2,fg_color="#154360",border_color="#707b7c",text="Owner Info",font=fontbtn,cursor="hand2",width=150,height=40)
ownerbtn.pack(padx=1,pady=5)
paymentbtn = ct.CTkButton(menuframe,image=payment_image,border_width=2,fg_color="#154360",border_color="#707b7c",text="Payments",
                          font=fontbtn,width=150,cursor="hand2",height=40,command=lambda:payments(app))
paymentbtn.pack()
reportbtn = ct.CTkButton(menuframe,image=report_image,border_width=2,fg_color="#154360",border_color="#707b7c",text="Reports",font=fontbtn,width=150,height=40,cursor="hand2")
reportbtn.pack(padx=1,pady=5)
Transferbtn = ct.CTkButton(menuframe,image=transfer_image,border_width=2,fg_color="#154360",border_color="#707b7c",text="Transfer",font=fontbtn,width=150,height=40,cursor="hand2")
Transferbtn.pack()
bifbtn = ct.CTkButton(menuframe,image=split_image,border_width=2,fg_color="#154360",border_color="#707b7c",text="Bifarcation",font=fontbtn,width=150,height=40,cursor="hand2")
bifbtn.pack(padx=1,pady=5)
exitbtn = ct.CTkButton(menuframe,image=switch_image,border_width=2,fg_color="#154360",border_color="#707b7c",text="Exit",font=fontbtn,width=150,height=40,cursor="hand2")
exitbtn.pack()

# End of Menu

# Dashboard
# Plot details

""" plotlable =ct.CTkLabel(plotdetailsframe,font=fontlmenu,text="Plot Details")
plotlable.pack() """





app.mainloop()