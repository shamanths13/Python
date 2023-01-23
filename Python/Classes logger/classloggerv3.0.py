import customtkinter
import json
from datetime import date
import os

'''
tdy_date=date.today()
tdy_day=date.weekday(tdy_date)
tdy_date=tdy_date.strftime("%d/%m/%Y")
'''
tdy_day=5
tdy_date="21/01/2023"

with open(os.path.join(os.path.dirname(__file__),"schedule.json"), 'r') as f:
    data = json.load(f)

new_day = {
    "date":tdy_date,
    "day":data[tdy_day]['day'],
    "classes":[]
}

new_data = {
    "section": "",
    "cond": "",
    "sch_time": "",
    "act_time": "",
    "hours": "",    
    "lesson": "",
    "remarks": ""
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


def create_class(section, time,n):

    name="Class "+str(n+1)    
    btn_text=section+"\nTime: "+time
    def seltab():
        def save():
            with open(os.path.join(os.path.dirname(__file__),"classesdone.json"), 'r+') as f:
                data_add = json.load(f)
                data_add[-1]["classes"][n]["cond"]=cond_entry.get()
                data_add[-1]["classes"][n]["act_time"]=act_time_entry.get()
                data_add[-1]["classes"][n]["hours"]=hrs_entry.get()
                data_add[-1]["classes"][n]["lesson"]=lesson_entry.get()
                data_add[-1]["classes"][n]["remarks"]=remarks_entry.get()
                f.seek(0)
                json.dump(data_add, f, indent = 4)
            tabview.delete(name)
        tab1=tabview.add(name)
        

        def tabn_exit():
            tabview.delete(name)


        cl_text="Time: "+time
        label_1 = customtkinter.CTkLabel(tab1,text=section ,font=('Arial', 16,"bold"))
        label_1.pack(pady=(0,0), padx=0)
        label_1 = customtkinter.CTkLabel(tab1,text=cl_text ,font=('Arial', 16,"bold"))
        label_1.pack(pady=(0,6), padx=0)

        with open(os.path.join(os.path.dirname(__file__),"classesdone.json"), 'r+') as f:
                data_add = json.load(f)

        cond_entry = customtkinter.CTkEntry(tab1,width=280,height=32,corner_radius=8,font=('Arial', 14,"bold"),fg_color=colour1,placeholder_text_color="gray30", placeholder_text="Class conducted: Y/N")
        cond_entry.pack(padx=2, pady=(0,0))
        if data_add[-1]["classes"][n]["cond"] != "":
            cond_entry.insert(0,data_add[-1]["classes"][n]["cond"])

        act_time_entry = customtkinter.CTkEntry(tab1,width=280,height=32,corner_radius=8,font=('Arial', 14,"bold"),fg_color=colour1,placeholder_text_color="gray30", placeholder_text="Enter the actual time")
        act_time_entry.pack(padx=2, pady=(2,0))
        if data_add[-1]["classes"][n]["act_time"] != "":
            act_time_entry.insert(0,data_add[-1]["classes"][n]["act_time"])

        hrs_entry = customtkinter.CTkEntry(tab1,width=280,height=32,corner_radius=8,font=('Arial', 14,"bold"),fg_color=colour1,placeholder_text_color="gray30", placeholder_text="Enter no. of hours")
        hrs_entry.pack(padx=2, pady=(2,0))
        if data_add[-1]["classes"][n]["hours"] != "":
            hrs_entry.insert(0,data_add[-1]["classes"][n]["hours"])

        lesson_entry = customtkinter.CTkEntry(tab1,width=280,height=32,corner_radius=8,font=('Arial', 14,"bold"),fg_color=colour1,placeholder_text_color="gray30", placeholder_text="Enter the lesson taught")
        lesson_entry.pack(padx=2, pady=(2,0))
        if data_add[-1]["classes"][n]["lesson"] != "":
            lesson_entry.insert(0,data_add[-1]["classes"][n]["lesson"])

        remarks_entry = customtkinter.CTkEntry(tab1,width=280,height=32,corner_radius=8,font=('Arial', 14,"bold"),fg_color=colour1,placeholder_text_color="gray30", placeholder_text="Enter any remarks")
        remarks_entry.pack(padx=2, pady=(2,0))
        if data_add[-1]["classes"][n]["remarks"] != "":
            lesson_entry.insert(0,data_add[-1]["classes"][n]["remarks"])
        
        buttonsave = customtkinter.CTkButton(tab1, hover=True, hover_color="lime green", width=60, height=10, fg_color="forest green",bg_color=colour, text="Save", text_color= "gray75", font=('Arial', 14,"bold"), corner_radius=8, command=save)
        buttonsave.pack(pady=(6,0), padx=0)

        buttonexit = customtkinter.CTkButton(tab1, hover=True, hover_color="red", width=60, height=10, fg_color=colour1,bg_color=colour, text="Cancel", text_color= "gray75",font=('Arial', 14,"bold"), corner_radius=8, command=tabn_exit)
        buttonexit.pack(padx=0, pady=(8,0))
        
        tabview.set(name)


    buttonclass = customtkinter.CTkButton(tabmain, hover=True, hover_color="forest green", width=280, height=50, fg_color="gray25",bg_color=colour, text=btn_text, text_color= "gray80", font=('Arial', 14,"bold"), corner_radius=8, command=seltab)
    buttonclass.pack(pady=(5,0), padx=0)

    
frame=customtkinter.CTkFrame(root, fg_color=colour1,bg_color="black",corner_radius=8)
frame.pack(pady=0,padx=0,fill="both",expand=True)

frame2=customtkinter.CTkFrame(frame, fg_color=colour,bg_color=colour1,corner_radius=8)
frame2.pack(pady=(5,0),padx=5,fill="both",expand=True)

buttonmove = customtkinter.CTkButton(frame2, hover=True, hover_color="lime green", width=33, height=23, fg_color=colour1,bg_color=colour, text="◎", text_color= colour, font=('Arial', 14,"bold"), corner_radius=8)
buttonmove.place(relx=0.0166, rely=0.15)

buttonexit = customtkinter.CTkButton(frame2, hover=True, hover_color="red", width=33, height=23, fg_color=colour1,bg_color=colour, text="X", text_color= colour,font=('Arial', 12,"bold"), corner_radius=8, command=root.quit)
buttonexit.place(relx=0.888, rely=0.15)

dt_text=data[tdy_day]['day']+"  "+tdy_date
label_1 = customtkinter.CTkLabel(frame2,width=240, text=str.upper(dt_text) ,font=('Arial', 20,"bold"))
label_1.pack(pady=(2,2), padx=50)

tabview = customtkinter.CTkTabview(frame,height=340, corner_radius=8,fg_color= colour, segmented_button_selected_color="mediumpurple4")
tabview.pack(padx=5, pady=(0,5), fill="both",expand=True)
tabmain=tabview.add("Schedule")
tabview.configure(state="disabled")


if tdy_day != 6 :
    for n, classes in enumerate(data_add[-1]['classes']):
        section=classes['section']
        time=classes['sch_time']
        create_class(section,time,n)
        tabview.set("Schedule")
else:
    for n, classes in enumerate(data_add[-1]['classes']):
        if n!=0:
            section=classes['section']
            time=classes['sch_time']
            create_class(section,time,n)
            tabview.set("Schedule")


def add_misc():
    tabn=tabview.add("New")
    def save_misc():
        with open(os.path.join(os.path.dirname(__file__),"classesdone.json"), 'r+') as f:
            data_add = json.load(f)
            data_add[-1]["classes"].append(new_data)
            f.seek(0)
            json.dump(data_add, f, indent = 4)
        with open(os.path.join(os.path.dirname(__file__),"classesdone.json"), 'r+') as f:
                data_add = json.load(f)
                data_add[-1]["classes"][-1]["section"]=new_section_entry.get()
                data_add[-1]["classes"][-1]["sch_time"]=new_sch_time_entry.get()
                data_add[-1]["classes"][-1]["cond"]=new_cond_entry.get()
                data_add[-1]["classes"][-1]["act_time"]=new_act_time_entry.get()
                data_add[-1]["classes"][-1]["hours"]=new_hrs_entry.get()
                data_add[-1]["classes"][-1]["lesson"]=new_lesson_entry.get()
                data_add[-1]["classes"][-1]["remarks"]=new_remarks_entry.get()
                f.seek(0)
                json.dump(data_add, f, indent = 4)
        tabview.delete("New")


    def new_exit():
        tabview.delete("New")


    label_w = customtkinter.CTkLabel(tabn,text="Enter Class Details" ,font=('Arial', 16,"bold"))
    label_w.pack(pady=(0,0), padx=50)

    new_section_entry = customtkinter.CTkEntry(tabn,width=280,height=28,corner_radius=8,font=('Arial', 14,"bold"),fg_color=colour1,placeholder_text_color="gray30", placeholder_text="Enter the Grade/Section")
    new_section_entry.pack(padx=2, pady=(0,0))
    
    new_sch_time_entry = customtkinter.CTkEntry(tabn,width=280,height=28,corner_radius=8,font=('Arial', 14,"bold"),fg_color=colour1,placeholder_text_color="gray30", placeholder_text="Enter the scheduled time")
    new_sch_time_entry.pack(padx=2, pady=(0,0))

    new_cond_entry = customtkinter.CTkEntry(tabn,width=280,height=28,corner_radius=8,font=('Arial', 14,"bold"),fg_color=colour1,placeholder_text_color="gray30", placeholder_text="Class conducted: Y/N")
    new_cond_entry.pack(padx=2, pady=(0,0))

    new_act_time_entry = customtkinter.CTkEntry(tabn,width=280,height=28,corner_radius=8,font=('Arial', 14,"bold"),fg_color=colour1,placeholder_text_color="gray30", placeholder_text="Enter the actual time")
    new_act_time_entry.pack(padx=2, pady=(0,0))

    new_hrs_entry = customtkinter.CTkEntry(tabn,width=280,height=28,corner_radius=8,font=('Arial', 14,"bold"),fg_color=colour1,placeholder_text_color="gray30", placeholder_text="Enter no. of hours")
    new_hrs_entry.pack(padx=2, pady=(0,0))

    new_lesson_entry = customtkinter.CTkEntry(tabn,width=280,height=28,corner_radius=8,font=('Arial', 14,"bold"),fg_color=colour1,placeholder_text_color="gray30", placeholder_text="Enter the lesson taught")
    new_lesson_entry.pack(padx=2, pady=(0,0))

    new_remarks_entry = customtkinter.CTkEntry(tabn,width=280,height=28,corner_radius=8,font=('Arial', 14,"bold"),fg_color=colour1,placeholder_text_color="gray30", placeholder_text="Enter any remarks")
    new_remarks_entry.pack(padx=2, pady=(0,0))

    buttonsave = customtkinter.CTkButton(tabn, hover=True, hover_color="lime green", width=60, height=10, fg_color="forest green",bg_color=colour, text="Save", text_color= "white", font=('Arial', 14,"bold"), corner_radius=8, command=save_misc)
    buttonsave.pack(pady=(7,9), padx=0)

    buttonexit = customtkinter.CTkButton(tabn, hover=True, hover_color="red", width=60, height=10, fg_color=colour1,bg_color=colour, text="Cancel", text_color= "gray75",font=('Arial', 14,"bold"), corner_radius=8, command=new_exit)
    buttonexit.pack(padx=2, pady=(0,0))

    tabview.set("New")
   
buttonsavemsc = customtkinter.CTkButton(tabmain, hover=True, hover_color="forest green", width=280, height=50, fg_color=colour1,bg_color=colour, text="Add Misc class", text_color= "gray75", font=('Arial', 14,"bold"), corner_radius=8, command=add_misc)
buttonsavemsc.pack(pady=(5,0), padx=0)


def moveMouseButton(e):
   root.geometry(f'+{e.x_root}+{e.y_root}')

buttonmove.bind("<B1-Motion>", moveMouseButton)

root.mainloop()
