import customtkinter
import json
from datetime import date
import os

'''
tdy_date=date.today()
tdy_day=date.weekday(tdy_date)
tdy_date=tdy_date.strftime("%d/%m/%Y")
'''
tdy_day=0
tdy_date="23-1-2023"

with open(os.path.join(os.path.dirname(__file__),"schedule.json"), 'r') as f:
    data = json.load(f)

new_day = {
    "date":tdy_date,
    "day":data[tdy_day]['day'],
    "classes":[]
}

new_data = {
    "section": "",
    "cond_remarks": "",
    "sch_time": "",
    "act_time": "",
    "hours": "",    
    "lesson": ""
}

check= False
with open(os.path.join(os.path.dirname(__file__),"classesdone.json"), 'r+') as f:
    data_add = json.load(f)
    if data_add[-1]['date'] != tdy_date:
        data_add.append(new_day)
        for n, classes in enumerate(data[tdy_day]['classes']):
            data_add[-1]["classes"].append(new_data)
        f.seek(0)
        json.dump(data_add, f, indent = 4)
        check= True

if check == True:
    for n, classes in enumerate(data[tdy_day]['classes']):
        with open(os.path.join(os.path.dirname(__file__),"classesdone.json"), 'r+') as f:
            data_add = json.load(f)
            data_add[-1]["classes"][n]["section"]=classes["section"]
            data_add[-1]["classes"][n]["sch_time"]=classes["time"]
            f.seek(0)
            json.dump(data_add, f, indent = 4)


with open(os.path.join(os.path.dirname(__file__),"classesdone.json"), 'r+') as f:
    data_add = json.load(f)
   
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root=customtkinter.CTk()
root.geometry()
root.title("Nova's Classes")
#root.iconbitmap(resource_path("chaosicon.ico"))
root.resizable(False,True)

root.overrideredirect(True)
root.wm_attributes('-transparentcolor',"black")
colour="gray35"
colour1="gray20"

def saved():
    window = customtkinter.CTkToplevel()
    window.geometry()
    window.resizable(False,False)
    window.overrideredirect(True)
    window.wm_attributes('-transparentcolor',"black")
    frame=customtkinter.CTkFrame(window, fg_color=colour1,bg_color="black",corner_radius=8)
    frame.pack(pady=0,padx=0,fill="both",expand=True)
    frame2=customtkinter.CTkFrame(frame, fg_color=colour,bg_color=colour1,corner_radius=8)
    frame2.pack(pady=5,padx=5,fill="both",expand=True)
    label_w = customtkinter.CTkLabel(frame2,text="Data saved!" ,font=('Arial', 20,"bold"))
    label_w.pack(pady=(2,2), padx=50)
    buttonexit = customtkinter.CTkButton(frame2, hover=True, hover_color="lime green", width=33, height=10, fg_color="forest green",bg_color=colour, text="Ok", text_color= "white", font=('Arial', 14,"bold"), corner_radius=8, command=window.destroy)
    buttonexit.pack(pady=(3,5), padx=0)
    pass


def create_class(section, time,n):

    def save():
        with open(os.path.join(os.path.dirname(__file__),"classesdone.json"), 'r+') as f:
            data_add = json.load(f)
            data_add[-1]["classes"][n]["cond_remarks"]=cond_entry.get()
            data_add[-1]["classes"][n]["act_time"]=act_time_entry.get()
            data_add[-1]["classes"][n]["hours"]=hrs_entry.get()
            data_add[-1]["classes"][n]["lesson"]=lesson_entry.get()
            f.seek(0)
            json.dump(data_add, f, indent = 4)
        #saved()


    frame1=customtkinter.CTkFrame(frame, fg_color=colour,bg_color=colour1,corner_radius=8)
    frame1.pack(pady=(0,5),padx=5,fill="both",expand=True)
    cl_text=section+"\nTime: "+time
    label_1 = customtkinter.CTkLabel(frame1,text=cl_text ,font=('Arial', 14,"bold"))
    label_1.pack(pady=(2,2), padx=0)

    cond_entry = customtkinter.CTkEntry(frame1,width=326,height=28,corner_radius=8,font=('Arial', 14,"bold"),fg_color=colour1,placeholder_text_color="gray30", placeholder_text="Class conducted: Y/N, Remarks")
    cond_entry.pack(padx=2, pady=(0,0))
    if data_add[-1]["classes"][n]["cond_remarks"] != "":
        cond_entry.insert(0,data_add[-1]["classes"][n]["cond_remarks"])

    act_time_entry = customtkinter.CTkEntry(frame1,width=326,height=28,corner_radius=8,font=('Arial', 14,"bold"),fg_color=colour1,placeholder_text_color="gray30", placeholder_text="Enter the actual time")
    act_time_entry.pack(padx=2, pady=(0,0))
    if data_add[-1]["classes"][n]["act_time"] != "":
        act_time_entry.insert(0,data_add[-1]["classes"][n]["act_time"])

    hrs_entry = customtkinter.CTkEntry(frame1,width=326,height=28,corner_radius=8,font=('Arial', 14,"bold"),fg_color=colour1,placeholder_text_color="gray30", placeholder_text="Enter no. of hours")
    hrs_entry.pack(padx=2, pady=(0,0))
    if data_add[-1]["classes"][n]["hours"] != "":
        hrs_entry.insert(0,data_add[-1]["classes"][n]["hours"])

    lesson_entry = customtkinter.CTkEntry(frame1,width=326,height=28,corner_radius=8,font=('Arial', 14,"bold"),fg_color=colour1,placeholder_text_color="gray30", placeholder_text="Enter the lesson taught")
    lesson_entry.pack(padx=2, pady=(0,0))
    if data_add[-1]["classes"][n]["lesson"] != "":
        lesson_entry.insert(0,data_add[-1]["classes"][n]["lesson"])
    
    buttonsave = customtkinter.CTkButton(frame1, hover=True, hover_color="lime green", width=33, height=10, fg_color=colour1,bg_color=colour, text="Save", text_color= "gray75", font=('Arial', 14,"bold"), corner_radius=8, command=save)
    buttonsave.pack(pady=(3,5), padx=0)
    

frame=customtkinter.CTkFrame(root, fg_color=colour1,bg_color="black",corner_radius=8)
frame.pack(pady=0,padx=0,fill="both",expand=True)

frame2=customtkinter.CTkFrame(frame, fg_color=colour,bg_color=colour1,corner_radius=8)
frame2.pack(pady=5,padx=5,fill="both",expand=True)

buttonmove = customtkinter.CTkButton(frame2, hover=True, hover_color="lime green", width=33, height=23, fg_color=colour1,bg_color=colour, text="◎", text_color= colour, font=('Arial', 14,"bold"), corner_radius=8)
buttonmove.place(relx=0.0166, rely=0.15)

buttonexit = customtkinter.CTkButton(frame2, hover=True, hover_color="red", width=33, height=23, fg_color=colour1,bg_color=colour, text="X", text_color= colour,font=('Arial', 12,"bold"), corner_radius=8, command=root.quit)
buttonexit.place(relx=0.888, rely=0.15)

dt_text=data[tdy_day]['day']+"  "+tdy_date
label_1 = customtkinter.CTkLabel(frame2,text=str.upper(dt_text) ,font=('Arial', 20,"bold"))
label_1.pack(pady=(2,2), padx=50)

if tdy_day != 6 :
    for n, classes in enumerate(data_add[-1]['classes']):
        section=classes['section']
        time=classes['sch_time']
        create_class(section,time,n)

def add_misc():
    def save_misc():
        with open(os.path.join(os.path.dirname(__file__),"classesdone.json"), 'r+') as f:
            data_add = json.load(f)
            data_add[-1]["classes"].append(new_data)
            f.seek(0)
            json.dump(data_add, f, indent = 4)
        with open(os.path.join(os.path.dirname(__file__),"classesdone.json"), 'r+') as f:
                data_add = json.load(f)
                data_add[-1]["classes"][-1]["section"]=section_entry.get()
                data_add[-1]["classes"][-1]["sch_time"]=sch_time_entry.get()
                f.seek(0)
                json.dump(data_add, f, indent = 4)
        window.destroy()

    window = customtkinter.CTkToplevel()
    window.geometry()
    window.resizable(False,False)
    window.overrideredirect(True)
    window.wm_attributes('-transparentcolor',"black")
    frame=customtkinter.CTkFrame(window, fg_color=colour1,bg_color="black",corner_radius=8)
    frame.pack(pady=0,padx=0,fill="both",expand=True)
    frame2=customtkinter.CTkFrame(frame, fg_color=colour,bg_color=colour1,corner_radius=8)
    frame2.pack(pady=5,padx=5,fill="both",expand=True)

    buttonexit = customtkinter.CTkButton(frame2, hover=True, hover_color="red", width=33, height=23, fg_color=colour1,bg_color=colour, text="X", text_color= colour,font=('Arial', 12,"bold"), corner_radius=8, command=window.destroy)
    buttonexit.place(relx=0.888, rely=0.05)

    label_w = customtkinter.CTkLabel(frame2,text="Enter Class Details" ,font=('Arial', 20,"bold"))
    label_w.pack(pady=(2,2), padx=50)

    section_entry = customtkinter.CTkEntry(frame2,width=326,height=28,corner_radius=8,font=('Arial', 14,"bold"),fg_color=colour1,placeholder_text_color="gray30", placeholder_text="Class conducted: Y/N, Remarks")
    section_entry.pack(padx=2, pady=(0,0))
    
    sch_time_entry = customtkinter.CTkEntry(frame2,width=326,height=28,corner_radius=8,font=('Arial', 14,"bold"),fg_color=colour1,placeholder_text_color="gray30", placeholder_text="Enter the actual time")
    sch_time_entry.pack(padx=2, pady=(0,0))

    buttonsave = customtkinter.CTkButton(frame2, hover=True, hover_color="lime green", width=33, height=10, fg_color="forest green",bg_color=colour, text="Save", text_color= "white", font=('Arial', 14,"bold"), corner_radius=8, command=save_misc)
    buttonsave.pack(pady=(3,5), padx=0)

   
frame3=customtkinter.CTkFrame(frame, fg_color=colour,bg_color=colour1,corner_radius=8)
frame3.pack(pady=(0,5),padx=5,fill="both",expand=True)

buttonsavemsc = customtkinter.CTkButton(frame3, hover=True, hover_color="lime green", width=33, height=10, fg_color="forest green",bg_color=colour, text="Add Misc class", text_color= "white", font=('Arial', 14,"bold"), corner_radius=8, command=add_misc)
buttonsavemsc.pack(pady=(5,5), padx=0)

def moveMouseButton(e):
   root.geometry(f'+{e.x_root}+{e.y_root}')

buttonmove.bind("<B1-Motion>", moveMouseButton)

root.mainloop()