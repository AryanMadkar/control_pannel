from tkinter import *
from tkinter import ttk
from tkinter import ttk,messagebox
import tkinter as tk
from tkinter import filedialog
import platform 
import psutil
import customtkinter as ctk

#brightness 
import screen_brightness_control as pct

#audio
from ctypes import cast,pointer
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities,IAudioEndpointVolume

#weather
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz

#clock
from time import strftime

#calender 
from tkcalendar import *

#open google
import pyautogui
import subprocess
import webbrowser as wb
import random


root= Tk()
root.title("mac-soft Tool")
root.geometry("850x500+300+170")
root.resizable(FALSE,False)
root.configure(bg="#131842")

image_icon = PhotoImage(file="first\Image\icon.png")
root.iconphoto(False,image_icon)

body = Frame(root,width=900,height=600,bg="#32012F")
body.pack(pady=20,padx=20)


lhs = Frame(body,width=310,height=435,bg="#E2DFD0",highlightbackground="black",highlightthickness="1")
lhs.place(x=10,y=10)

#logo
photo=PhotoImage(file="first\Image\laptop.png")
myimage = Label(lhs,image=photo,background="#E2DFD0")
myimage.place(x=1,y=20)


my_system = platform.uname()
l1 = Label(lhs,text=f"Name:{my_system.node}",bg="#E2DFD0",font=("Acumin Variable Concept",15,"bold"),justify="center")
l1.place(x=15,y=210)

l2 = Label(lhs,text=f"Version:{my_system.version}",bg="#E2DFD0",font=("Acumin Variable Concept",8),justify="center")
l2.place(x=15,y=240)

l3 = Label(lhs,text=f"System:{my_system.system}",bg="#E2DFD0",font=("Acumin Variable Concept",15),justify="center")
l3.place(x=15,y=260)

l4 = Label(lhs,text=f"Machine:{my_system.machine}",bg="#E2DFD0",font=("Acumin Variable Concept",15),justify="center")
l4.place(x=15,y=285)

l5 = Label(lhs,text=f"RAM installed:{round(psutil.virtual_memory().total/1000000000,2)} GB",bg="#E2DFD0",font=("Acumin Variable Concept",15),justify="center")
l5.place(x=15,y=310)

l6 = Label(lhs,text=f"Processor:{my_system.processor}",bg="#E2DFD0",font=("Acumin Variable Concept",7),justify="center")
l6.place(x=15,y=350)

Rhs = Frame(body,width=470,height=230,bg="#E2DFD0",highlightbackground="black",highlightthickness="1")
Rhs.place(x=330,y=10)


system = Label(Rhs,text="System",font=("Acumin Variable Concept",15),bg="#E2DFD0")
system.place(x=10,y=10)

################Battery##################

def convertTime(seconds):
    minutes, seconds = divmod(seconds, 60) 
    hours, minutes = divmod(minutes, 60) 
    return "%d:%02d:%02d" % (hours, minutes, seconds) 
    


def none():
    
    global battery_png
    global battery_label
    battery = psutil.sensors_battery() 
    percentage = battery.percent
    time = convertTime(battery.secsleft)
    print(percentage)
    lbl1.config(text=f"{percentage}%")
    lbl_plug.config(text=f"Plug in: {str(battery.power_plugged)}")
    lbl_time.config(text=f"{time}remaining")
    
    battery_label = Label(Rhs,background="#E2DFD0")
    battery_label.place(x=15,y=50)
    
    lbl1.after(1000,none)
    
    if battery.power_plugged == True:
        battery_png = PhotoImage(file="first\Image/battery.png")
        battery_label.config(image=battery_png)
    else:    
        battery_png = PhotoImage(file="first\Image\charging.png")
        battery_label.config(image=battery_png)
    

lbl1 = Label(Rhs,font=("Acumin Variable Concept",40,"bold"),bg="#E2DFD0")
lbl1.config(text="")
lbl1.place(x=200,y=40)

lbl_plug = Label(Rhs,font=("Acumin Variable Concept",10,"bold"),bg="#E2DFD0")
lbl_plug.config(text="")
lbl_plug.place(x=20,y=100)

lbl_time = Label(Rhs,font=("Acumin Variable Concept",15,"bold"),bg="#E2DFD0")
lbl_time.config(text="")
lbl_time.place(x=200,y=100)




############################################

#########speaker###################

lbl_speaker = Label(Rhs, text="Speaker:  ",font=("Acumin Variable Concept",15,"bold"),bg="#E2DFD0")
lbl_speaker.place(x=10,y=150)
volume_value = tk.DoubleVar()

def get_current_volume_value():
    return"{:.2f}".format(volume_value.get())

def volume_changed():
    device = AudioUtilities.GetSpeakers()
    interface = device.Activate(IAudioEndpointVolume._iid_,CLSCTX_ALL,None)
    volume = cast(interface,pointer(IAudioEndpointVolume))
    volume.setMasterVolumeLevel(-float(get_current_volume_value()),None)
    
style = ttk.Style()
style.configure("TScale",background="#E2DFD0")

volume = ttk.Scale(Rhs,from_=60,to=0,orient="horizontal",command=volume_changed,variable=volume_value,cursor="hand2")
volume.place(x=100,y=155)
volume.set(20)







########################################

#######################Brightness#######################



lbl_brightness = Label(Rhs,text="Brightness: ",font=("Acumin Variable Concept",15,"bold"),bg="#E2DFD0")
lbl_brightness.place(x=10,y=190)

current_value=tk.DoubleVar()

def get_current_value():
    return "{:.2f}".format(current_value.get())

def brightness_changed(event):
    pct.set_brightness(get_current_value())

brightness =ttk.Scale(Rhs, from_= 0, to=100,orient = "horizontal",command=brightness_changed,variable=current_value,cursor="hand2")
brightness.place(x=140,y=190)






##########################################################3

Rhb = Frame(body,width=470,height=190,bg="#E2DFD0",highlightbackground="black",highlightthickness="1")
Rhb.place(x=330,y=255)

apps =Label(Rhb,text="Apps",font=("Acumin Variable Concept",15,"bold"),bg="#E2DFD0")
apps.place(x=10,y=10)

def weather():
    app1 = Toplevel()
    app1.geometry("850x500+300+170")
    app1.title("Weather")
    app1.config(bg="#0C1844")
    app1.resizable(False,False)
    
    #icon
    app_icon = PhotoImage(file="first\Image\App1.png")
    app1.iconphoto(False,app_icon)
    
    from geopy.geocoders import Nominatim
    
    def getweather():
        try:
            city = textfield.get()
            geolocator = Nominatim(user_agent="geoapiExercises")
            location = geolocator.getcode(city)
            obj=TimezoneFinder()
            result = obj.timezone_at(lng=location.longitude,lat=location.latitude)
            
            home=pytz.timezone(result)
            local_time=datetime.now(home)
            current_time=local_time.strftime("%I:%M:%P")
            clock.config(text=current_time)
            name.config(text="CURRENT WEATHER")
            
            #weather
            api = "https://api.openweathermap.org/data/2.5/weather?q="+city"&appid=646824f2b7b86caffec1d0b16ea77f79"
        except Exception as e:
            messagebox.showerror("Weather App","invalid Entry!!")
    
    
    #search box
    
    Search_image = PhotoImage(file="first\Image\search.png")
    myimage = Label(app1,image=Search_image,bg="#0C1844")
    myimage.place(x=20,y=20)
    
    textfield = tk.Entry(app1,justify="center",width=23,font=("poppins",16,"bold"),bg="#0F121B",border=0,fg="white")
    textfield.place(x=53,y=40)
    textfield.focus()
    
    
    search_icon = PhotoImage(file="first\Image\search_icon.png")
    myimage_icon = Button(app1,image=search_icon,borderwidth=0,height=38,cursor="hand2",bg="#0F121B",command=getweather)
    myimage_icon.place(x=400,y=40)
    
    ############logo##########
    
    logo_image = PhotoImage(file="first\Image\logo.png")
    logo = Label(app1,image=logo_image,bg="#0C1844")
    logo.place(x=150,y=100)
    
    
    #############bottom Box################
    Frame_image = PhotoImage(file="first\Image/box.png")
    frame_myimage = Label(app1,image=Frame_image,bg="#0C1844")
    frame_myimage.pack(padx=5,pady=5,side=BOTTOM)
    
    #time
    name = Label(app1,font=("arial",15,"bold"),bg="#0C1844")
    name.place(x=30,y=100)
    clock=Label(app1,font=("Helvetica",20),bg="#0C1844")
    clock.place(x=30,y=130)
    
    #labe
    label1 = Label(app1,text="WIND",font=("Helvetica",15,"bold"),fg="Black",bg="#019ddc")
    label1.place(x=120,y=400)
    
    label2 = Label(app1,text="HUMIDITY",font=("Helvetica",15,"bold"),fg="Black",bg="#019ddc")
    label2.place(x=250,y=400)
    
    label3 = Label(app1,text="DESCRIPTION",font=("Helvetica",15,"bold"),fg="Black",bg="#019ddc")
    label3.place(x=430,y=400)
    
    label4 = Label(app1,text="PRESSURE",font=("Helvetica",15,"bold"),fg="Black",bg="#019ddc")
    label4.place(x=650,y=400)
    
    # t=Label(app1,text="lion",font=("arial",20,"bold"),fg="ee666d",bg="#0C1844")
    # t.place(x=400,y=150)
    
    # c = Label(app1,text="pig",font=("arial",20,"bold"),bg="#019ddc")
    # c.place(x=400,y=250)
    
    w=Label(app1,text="...",font=("arial",20,"bold"),bg="#019ddc")
    w.place(x=120,y=430)
    
    h=Label(app1,text="...",font=("arial",20,"bold"),bg="#019ddc")
    h.place(x=280,y=430)
    
    d=Label(app1,text="...",font=("arial",20,"bold"),bg="#019ddc")
    d.place(x=450,y=430)
    
    p=Label(app1,text="...",font=("arial",20,"bold"),bg="#019ddc")
    p.place(x=670,y=430)
    
   
    
    
    app1.mainloop()
    
def clock():
    app1 = Toplevel()
    app1.geometry("850x500+300+170")
    app1.title("Weather")
    app1.config(bg="#f4f5f5")
    app1.resizable(False,False)
    
    
    
    app1.mainloop()
    
def calander():
    app1 = Toplevel()
    app1.geometry("850x500+300+170")
    app1.title("Weather")
    app1.config(bg="#f4f5f5")
    app1.resizable(False,False)
    
    
    
    app1.mainloop()

app1_img = PhotoImage(file="first\Image\App1.png")
app1 = Button(Rhb,image=app1_img,bd=0,bg="#E2DFD0",cursor="hand2",command=weather)
app1.place(x=15,y=50)

app2_img = PhotoImage(file="first\Image\App2.png")
app2 = Button(Rhb,image=app2_img,bd=0,bg="#E2DFD0",cursor="hand2" ,command=clock)
app2.place(x=100,y=50)

app3_img = PhotoImage(file="first\Image\App3.png")
app3 = Button(Rhb,image=app3_img,bd=0,bg="#E2DFD0",cursor="hand2",command=calander)
app3.place(x=185,y=50)

app4_img = PhotoImage(file="first\Image\App4.png")
app4 = Button(Rhb,image=app4_img,bd=0,bg="#E2DFD0",cursor="hand2")
app4.place(x=270,y=50)

app5_img = PhotoImage(file="first\Image\App5.png")
app5 = Button(Rhb,image=app5_img,bd=0,bg="#E2DFD0",cursor="hand2")
app5.place(x=355,y=50)

app6_img = PhotoImage(file="first\Image\App6.png")
app6 = Button(Rhb,image=app6_img,bd=0,bg="#E2DFD0",cursor="hand2")
app6.place(x=15,y=120)


app7_img = PhotoImage(file="first\Image\App7.png")
app7 = Button(Rhb,image=app7_img,bd=0,bg="#E2DFD0",cursor="hand2")
app7.place(x=100,y=120)


app8_img = PhotoImage(file="first\Image\App8.png")
app8 = Button(Rhb,image=app8_img,bd=0,bg="#E2DFD0",cursor="hand2")
app8.place(x=185,y=120)


app9_img = PhotoImage(file="first\Image\App9.png")
app9 = Button(Rhb,image=app9_img,bd=0,bg="#E2DFD0",cursor="hand2")
app9.place(x=270,y=120)

app10_img = PhotoImage(file="first\Image\App10.png")
app10 = Button(Rhb,image=app10_img,bd=0,bg="#E2DFD0",cursor="hand2")
app10.place(x=355,y=120)



none()


root.mainloop()
