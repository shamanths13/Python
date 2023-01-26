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

frame2=customtkinter.CTkFrame(frame,width=100, fg_color=colour,bg_color=colour1,corner_radius=8)
frame2.pack(pady=(5,0),padx=5,expand=True,side="left")

def create_day(day,n):

    def edit_day():
        for child in frame2.winfo_children():
            child.configure(state='disabled')
        buttonday.configure(fg_color="blue")
        def save_back():
            buttonday.configure(fg_color=colour1)
            frame2a.destroy()
            for child in frame2.winfo_children():
                child.configure(state='normal')
            
        def edit_class(classes,m):
            def save_class():
                day[m]

                pass


            def delete_class():
                del day_dict[m]
                print(day_dict)
                frame4.destroy()
                pass
            

            frame4=customtkinter.CTkFrame(frame2a, fg_color=colour1,bg_color=colour,corner_radius=8)
            frame4.pack(pady=(5,0),padx=5,fill="both",expand=True)

            new_section_entry = customtkinter.CTkEntry(frame4,width=280,height=28,corner_radius=8,font=('Arial', 14,"bold"),fg_color=colour1,placeholder_text_color="gray30", placeholder_text="Enter the Grade/Section")
            new_section_entry.pack(padx=2, pady=(0,0))
            new_section_entry.insert(0,classes["section"])
    
            new_sch_time_entry = customtkinter.CTkEntry(frame4,width=280,height=28,corner_radius=8,font=('Arial', 14,"bold"),fg_color=colour1,placeholder_text_color="gray30", placeholder_text="Enter the scheduled time")
            new_sch_time_entry.pack(padx=2, pady=(0,0))
            new_sch_time_entry.insert(0,classes["time"])

            buttonsave = customtkinter.CTkButton(frame4, hover=True, hover_color="lime green", width=60, height=10, fg_color="forest green",bg_color=colour, text="Save", text_color= "white", font=('Arial', 14,"bold"), corner_radius=8, command=save_class)
            buttonsave.pack(pady=(7,9), padx=0)

            buttonexit = customtkinter.CTkButton(frame4, hover=True, hover_color="red", width=60, height=10, fg_color=colour1,bg_color=colour, text="Cancel", text_color= "gray75",font=('Arial', 14,"bold"), corner_radius=8, command=delete_class)
            buttonexit.pack(padx=2, pady=(0,0))
            pass

        frame2a=customtkinter.CTkFrame(frame,width=200, fg_color=colour1,bg_color=colour,corner_radius=8)
        frame2a.pack(pady=(5,0),padx=5,side="top")

        buttonexit = customtkinter.CTkButton(frame2a, hover=True, hover_color="red", width=60, height=10, fg_color=colour1,bg_color=colour, text="Cancel", text_color= "gray75",font=('Arial', 14,"bold"), corner_radius=8, command=save_back)
        buttonexit.pack(padx=2, pady=(0,0))

        for m,classes in enumerate(day_dict):
            edit_class(classes,m)
        pass
    
    day_dict=day["classes"]
    print(day_dict)

    buttonday = customtkinter.CTkButton(frame2, hover=True, hover_color="lime green",  width=60,height=30, fg_color=colour1,bg_color=colour, text=day["day"], text_color= "white", font=('Arial', 14,"bold"), corner_radius=8, command=edit_day)
    buttonday.pack(pady=(7,9), padx=10,fill="both",expand=True)
    pass


for n,day in enumerate(data):
    create_day(day,n)


def moveMouseButton(e):
   root.geometry(f'+{e.x_root}+{e.y_root}')

buttonmove.bind("<B1-Motion>", moveMouseButton)

root.mainloop()
