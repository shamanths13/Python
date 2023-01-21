import customtkinter
import tkinter as ttk
import json
from datetime import date
import os

tdy_date=date.today()
tdy_day=date.weekday(tdy_date)
tdy_date=tdy_date.strftime("%d/%m/%Y")

with open(os.path.join(os.path.dirname(__file__),"schedule.json"), 'r') as f:
    data = json.load(f)

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root=customtkinter.CTk()
root.geometry("360x400")
root.title("Nova's Classes")
#root.iconbitmap(resource_path("chaosicon.ico"))
root.resizable(False,True)

root.overrideredirect(True)
root.wm_attributes('-transparentcolor',"black")
colour="gray30"
colour1="gray20"

frame=customtkinter.CTkFrame(root, fg_color=colour1,bg_color="black",corner_radius=8)
frame.pack(pady=0,padx=0,fill="both",expand=True)

label_1 = customtkinter.CTkLabel(frame,text="TODAY'S SCHEDULE" ,font=('Arial', 26,"bold"))
label_1.pack(pady=(20,20), padx=0)

dt_text=data[tdy_day]['day']+"  "+tdy_date
label_1 = customtkinter.CTkLabel(frame,text=dt_text ,font=('Arial', 18,"bold"))
label_1.pack(pady=(0,10), padx=0)

for classes in data[tdy_day]['classes']:
    cl_text=classes['section']+"\nTime: "+classes['time']
    label_1 = customtkinter.CTkLabel(frame,text=cl_text ,font=('Arial', 18,"bold"))
    label_1.pack(pady=(10,10), padx=0)

buttonexit = customtkinter.CTkButton(root, hover=True, hover_color="orangered3", width=33, height=23, fg_color=colour1,bg_color=colour1, text="X", text_color= colour1,font=('Arial', 12,"bold"), corner_radius=8, command=root.quit)
buttonexit.place(relx=0.940, rely=0.038, anchor=customtkinter.CENTER)

buttonmove = customtkinter.CTkButton(root, hover=True, hover_color="dark olive green", width=33, height=23, fg_color=colour1,bg_color=colour1, text="◎", text_color= colour1, font=('Arial', 14,"bold"), corner_radius=8)
buttonmove.place(relx=0.060, rely=0.038, anchor=customtkinter.CENTER)

def moveMouseButton(e):
   root.geometry(f'+{e.x_root}+{e.y_root}')

buttonmove.bind("<B1-Motion>", moveMouseButton)

root.mainloop()
