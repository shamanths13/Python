import customtkinter
import json
from datetime import date
import os

tdy_date=date.today()
tdy_day=date.weekday(tdy_date)
tdy_date=tdy_date.strftime("%d/%m/%Y")

with open(os.path.join(os.path.dirname(__file__),"schedule.json"), 'r') as f:
    data = json.load(f)


new_data = {
    "id": "",    
    "section": "",
    "time": ""            
}


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root=customtkinter.CTk()
root.geometry("350x400")
root.title("Nova's Classes")
#root.iconbitmap(resource_path("chaosicon.ico"))
root.resizable(False,True)

root.overrideredirect(True)
root.wm_attributes('-transparentcolor',"black")
colour="gray35"
colour1="gray20"

   
frame=customtkinter.CTkFrame(root, fg_color=colour1,bg_color="black",corner_radius=8)
frame.pack(pady=0,padx=0,fill="both",expand=True)

frame1=customtkinter.CTkFrame(frame,height=60, fg_color=colour,bg_color=colour1,corner_radius=8)
frame1.pack(pady=(5,0),padx=5)

label_1 = customtkinter.CTkLabel(frame1,width=240, text="Schedule Editor" ,font=('Arial', 20,"bold"))
label_1.pack(pady=(2,2), padx=50)

buttonmove = customtkinter.CTkButton(frame1, hover=True, hover_color="lime green", width=33, height=23, fg_color=colour1,bg_color=colour, text="◎", text_color= colour, font=('Arial', 14,"bold"), corner_radius=8)
buttonmove.place(relx=0.0166, rely=0.15)

buttonexit = customtkinter.CTkButton(frame1, hover=True, hover_color="red", width=33, height=23, fg_color=colour1,bg_color=colour, text="X", text_color= colour,font=('Arial', 12,"bold"), corner_radius=8, command=root.quit)
buttonexit.place(relx=0.888, rely=0.15)

tabview = customtkinter.CTkTabview(frame,height=(340), corner_radius=8,fg_color= colour, segmented_button_selected_color="mediumpurple4")
tabview.pack(padx=5, pady=(0,5), fill="both",expand=True)

tabmain=tabview.add("Schedule")
tabview.configure(state="disabled")

def create_day(day,n):

    def edit_day():
        tabn=tabview.add(day["day"])

        def class_add():
            pass

        def create_class(classes,m):
            def edit_class():

                def class_save():
                    data[n]["classes"][m]["section"]=section_entry.get()
                    data[n]["classes"][m]["sch_time"]=time_entry.get()
                    tabview.delete("Edit Class")
                    tabview.delete(day["day"])
                    edit_day()

                    pass

                def class_del():
                    del data[n]["classes"][m]
                    tabview.delete("Edit Class")
                    tabview.delete(day["day"])
                    edit_day()
                    pass


                tabc=tabview.add("Edit Class")
                frameca=customtkinter.CTkFrame(tabc, fg_color=colour1,bg_color=colour,corner_radius=8)
                frameca.pack(pady=(0,0),padx=5,fill="both",expand=True)

                section_entry = customtkinter.CTkEntry(frameca,width=280,height=32,corner_radius=8,font=('Arial', 14,"bold"),fg_color=colour1,placeholder_text_color="gray30", placeholder_text="Enter any remarks")
                section_entry.pack(padx=2, pady=(15,0))
                section_entry.insert(0,classes["section"])

                time_entry = customtkinter.CTkEntry(frameca,width=280,height=32,corner_radius=8,font=('Arial', 14,"bold"),fg_color=colour1,placeholder_text_color="gray30", placeholder_text="Enter any remarks")
                time_entry.pack(padx=2, pady=(15,0))
                time_entry.insert(0,classes["time"])

                class_savebtn = customtkinter.CTkButton(frameca, hover=True, hover_color="lime green",  width=60,height=30, fg_color=colour1,bg_color=colour, text="Save", text_color= "white", font=('Arial', 14,"bold"), corner_radius=8, command=class_save)
                class_savebtn.pack(pady=(7,9), padx=10,fill="both",expand=True)

                class_delbtn = customtkinter.CTkButton(frameca, hover=True, hover_color="lime green",  width=60,height=30, fg_color=colour1,bg_color=colour, text="Delete", text_color= "white", font=('Arial', 14,"bold"), corner_radius=8, command=class_del)
                class_delbtn.pack(pady=(7,9), padx=10,fill="both",expand=True)

                tabview.set("Edit Class")
                
            framec=customtkinter.CTkFrame(tabn, fg_color=colour1,bg_color=colour,corner_radius=8)
            framec.pack(pady=(5,0),padx=5,fill="both",expand=True)

            class_name=classes["section"]+"\nTime: "+classes["time"]

            buttonclass = customtkinter.CTkButton(framec, hover=True, hover_color="lime green",  width=60,height=30, fg_color=colour1,bg_color=colour, text=class_name, text_color= "white", font=('Arial', 14,"bold"), corner_radius=8, command=edit_class)
            buttonclass.pack(pady=(7,9), padx=10,fill="both",expand=True)

            pass

        def save_back():
            tabview.delete(day["day"])
            pass

        buttonadd = customtkinter.CTkButton(tabn, hover=True, hover_color="red", width=60, height=10, fg_color=colour1,bg_color=colour, text="Add New Class", text_color= "gray75",font=('Arial', 14,"bold"), corner_radius=8, command=class_add)
        buttonadd.pack(padx=2, pady=(0,0))

        for m,classes in enumerate(data[n]["classes"]):
            create_class(classes,m)

        buttonexit = customtkinter.CTkButton(tabn, hover=True, hover_color="red", width=60, height=10, fg_color=colour1,bg_color=colour, text="Cancel", text_color= "gray75",font=('Arial', 14,"bold"), corner_radius=8, command=save_back)
        buttonexit.pack(padx=2, pady=(0,0))

        tabview.set(day["day"])
    
    day_dict=day["classes"]
    print(day_dict)

    buttonday = customtkinter.CTkButton(tabmain, hover=True, hover_color="lime green",  width=60,height=30, fg_color=colour1,bg_color=colour, text=day["day"], text_color= "white", font=('Arial', 14,"bold"), corner_radius=8, command=edit_day)
    buttonday.pack(pady=(7,9), padx=10,fill="both",expand=True)
    pass


for n,day in enumerate(data):
    create_day(day,n)


def moveMouseButton(e):
   root.geometry(f'+{e.x_root}+{e.y_root}')

buttonmove.bind("<B1-Motion>", moveMouseButton)

root.mainloop()
