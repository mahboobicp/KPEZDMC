import customtkinter as ct
import tkinter
from PIL import Image
from tkinter import ttk
import plotallotment as plt
from plotallotment import pltallotment 
from industries import industries
from payments import payments
import dashboard as dash
from operations import operations
import database as db
from backend import backend
from reports import reports
from tkinter import messagebox
def image_read(path):
    open_image = Image.open(path)
    image = ct.CTkImage(open_image)
    return image
def image_read_logo(path):
    open_image = Image.open(path)
    image = ct.CTkImage(open_image,size=(100,100))
    return image
def button_click(button):
    global highlighted_button  # Keep track of the currently highlighted button

    # If there is a previously highlighted button, reset its appearance
    if highlighted_button is not None and highlighted_button != button:
        highlighted_button.configure(fg_color="#013d42",border_color="#04747e",text_color="white")  # Reset color of previous button bg_color="#212f3c",border_color="#04747e",font=fontbtn
    
    # Highlight the clicked button
    button.configure(fg_color="white",border_color="red",text_color="#001c1f")  # Change color of clicked button
    highlighted_button = button  # Update the highlighted button
#Allotment Button Clicked
def pltallotment_button(app,allotmentbtn):
    pltallotment(app)
    button_click(allotmentbtn)
def industries_button(app,industrybtn):
    industries(app)
    button_click(industrybtn)
def operations_button(app,operationbtn):
    operations(app)
    button_click(operationbtn)
def payments_button(app,paymentbtn):
    payments(app)
    button_click(paymentbtn)
def transfer_button(app,Transferbtn):
    button_click(Transferbtn)
def reports_button(app,reportbtn):
    reports(app)
    button_click(reportbtn)
def backend_button(app,bifbtn):
    backend(app)
    button_click(bifbtn)
def dashboard_button(app,homebtn):
    dash.dashboard(app)
    button_click(homebtn)
def close_app():
    # Show a confirmation dialog
    answer = messagebox.askyesno("Exit", "Are you sure you want to close the application?")
    
    # If user clicks "Yes", close the window
    if answer:
        app.destroy()
highlighted_button = None
fontlable = ("Open Sans",14)
fontlmenu = ("Poppins",18,"bold")
fontdash = ("Poppins",24,"bold")
fontentry = ("Arial",10,"bold")
fontbtn = ("Arial",16,"bold")
dfonts = ("Poppins",40,"bold")
fnt = ("Open Sans",14)
app =ct.CTk()
app.geometry("1020x662+200+5")
app.resizable(0,0)
app.config(background="#001c1f")
app.title("KPEZDMC IMS")
image_path_logo = r"D:\Python\KPEZDMC\images\industry.png"
logo_image = Image.open(image_path_logo)
logo_image = ct.CTkImage(logo_image)
#logo_image = tkinter.PhotoImage(file=r"D:\Python\KPEZDMC\images\industry.png")
headings = ct.CTkLabel(app,width=1180,image=image_read(r"D:\Python\KPEZDMC\images\industry.png"),compound="left",height=60,text=" KPEZDMC Industries Information System",
                       font=("Poppins",28,"bold"),text_color="#f8f9f9",fg_color="#001c1f",anchor="w")

headings.grid(row=0,column=0,columnspan=5,sticky="w")

titlebar = ct.CTkLabel(app,width=1180,height=20,text="WELCOME : Mahboob Ur Rahman \t\t\t\t\t Time : 00-00-00",
                       font=("Arial",14,"bold"),text_color="#f8f9f9",fg_color="#025c64")
titlebar.grid(row=1,column=0,columnspan=5,sticky="ew",padx=(0,300))
menuframe = ct.CTkFrame(app,fg_color="#013d42",bg_color="#013d42",corner_radius=200,width=200,height=362)
menuframe.place(x=1,y=82)
# Start of menu Frame
dash.dashboard(app)
# Use the function to load all the image_read(path)
photo_image = image_read_logo(r"D:\Python\KPEZDMC\images\logo.png")
home_image = image_read(r"D:\Python\KPEZDMC\images\home.png")
#tkinter.PhotoImage(file=r"D:\Python\KPEZDMC\images\home.png")
alt_image = image_read(r"D:\Python\KPEZDMC\images\alt.png")
#tkinter.PhotoImage(file=r"D:\Python\KPEZDMC\images\alt.png")
factory_image = image_read(r"D:\Python\KPEZDMC\images\factory1.png")
#tkinter.PhotoImage(file=r"D:\Python\KPEZDMC\images\factory1.png")
operation_image = image_read(r"D:\Python\KPEZDMC\images\operation.png")
#tkinter.PhotoImage(file=r"D:\Python\KPEZDMC\images\operation.png")
report_image = image_read(r"D:\Python\KPEZDMC\images\report.png")
#tkinter.PhotoImage(file=r"D:\Python\KPEZDMC\images\report.png")
payment_image = image_read(r"D:\Python\KPEZDMC\images\payment1.png")
#tkinter.PhotoImage(file=r"D:\Python\KPEZDMC\images\payment1.png")
transfer_image = image_read(r"D:\Python\KPEZDMC\images\transfer.png")
#tkinter.PhotoImage(file=r"D:\Python\KPEZDMC\images\transfer.png")
switch_image = image_read(r"D:\Python\KPEZDMC\images\switch.png")
#tkinter.PhotoImage(file=r"D:\Python\KPEZDMC\images\switch.png")
split_image = image_read(r"D:\Python\KPEZDMC\images\backend.png")
#tkinter.PhotoImage(file=r"D:\Python\KPEZDMC\images\backend.png")
logimage =ct.CTkLabel(menuframe,image=photo_image,width=40,height=40,text="",anchor="e")
logimage.pack(padx=(20,20),pady=(20,20))
menulable = ct.CTkLabel(menuframe,text="Menu",font=fontlmenu,text_color="#f8f9f9",corner_radius=50,
                        bg_color="#04747e",width=150,height=40)
menulable.pack()
homebtn = ct.CTkButton(menuframe,image=home_image,text="Home",border_width=2,fg_color="#013d42",hover_color="#04747e",
                       bg_color="#212f3c",border_color="#04747e",font=fontbtn,width=150,
                            height=40,cursor="hand2",command=lambda:dashboard_button(app,homebtn))
homebtn.pack(padx=3,pady=2)

allotmentbtn = ct.CTkButton(menuframe,image=alt_image,text="Allotment",border_width=2,fg_color="#013d42",hover_color="#04747e",
                       bg_color="#212f3c",border_color="#04747e",font=fontbtn,width=150,
                            height=40,cursor="hand2",command=lambda:pltallotment_button(app,allotmentbtn))
allotmentbtn.pack(padx=3,pady=2)
industrybtn = ct.CTkButton(menuframe,image=factory_image,border_width=2,fg_color="#013d42",hover_color="#04747e",
                       bg_color="#212f3c",border_color="#04747e",
                           text="Industries",cursor="hand2",font=fontbtn,width=150,height=40,
                           command=lambda:industries_button(app,industrybtn))
industrybtn.pack(pady=2)
operationbtn = ct.CTkButton(menuframe,image=operation_image,border_width=2,fg_color="#013d42",hover_color="#04747e",
                       bg_color="#212f3c",border_color="#04747e",
                            text="Opertions",font=fontbtn,cursor="hand2",width=150,height=40,command=lambda:operations_button(app,operationbtn))
operationbtn.pack(padx=1,pady=2)
paymentbtn = ct.CTkButton(menuframe,image=payment_image,border_width=2,fg_color="#013d42",hover_color="#04747e",
                       bg_color="#212f3c",border_color="#04747e",text="Payments",
                          font=fontbtn,width=150,cursor="hand2",height=40,command=lambda:payments_button(app,paymentbtn))
paymentbtn.pack(pady=2)
reportbtn = ct.CTkButton(menuframe,image=report_image,border_width=2,fg_color="#013d42",hover_color="#04747e",
                       bg_color="#212f3c",border_color="#04747e",text="Reports",
                       font=fontbtn,width=150,height=40,cursor="hand2",command=lambda:reports_button(app,reportbtn))
reportbtn.pack(padx=1,pady=2)
Transferbtn = ct.CTkButton(menuframe,image=transfer_image,border_width=2,fg_color="#013d42",hover_color="#04747e",
                       bg_color="#212f3c",border_color="#04747e",text="Transfer",font=fontbtn,width=150,
                       height=40,cursor="hand2",command=lambda:transfer_button(app,Transferbtn))
Transferbtn.pack()
bifbtn = ct.CTkButton(menuframe,image=split_image,border_width=2,fg_color="#013d42",hover_color="#04747e",
                       bg_color="#212f3c",border_color="#04747e",text="Backend",font=fontbtn,width=150,
                       height=40,cursor="hand2",command=lambda:backend_button(app,bifbtn))
bifbtn.pack(padx=1,pady=2)
exitbtn = ct.CTkButton(menuframe,image=switch_image,border_width=2,fg_color="#013d42",hover_color="red",
                       bg_color="#212f3c",border_color="#04747e",text="Exit",
                       font=fontbtn,width=150,height=40,cursor="hand2",command=lambda:close_app())
exitbtn.pack(pady=(2,10))

# End of Menu

# Dashboard
# Plot details

""" plotlable =ct.CTkLabel(plotdetailsframe,font=fontlmenu,text="Plot Details")
plotlable.pack() """





app.mainloop()