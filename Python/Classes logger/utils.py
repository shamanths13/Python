import customtkinter
import json
import os

with open(os.path.join(os.path.dirname(__file__),"classesdone.json"), 'r') as f:
    data = json.load(f)

total=0
hrs_total=0
min_total=0
min_total_rnd=0
hrs_min=[]
for n in range(len(data)):
    for m in range(len(data[n]["classes"])):
        chk=data[n]["classes"][m]["cond"]
        hrs=data[n]["classes"][m]["hours"]
        if chk == "Y":           
            total=total+1
            hrs_min=hrs.split(":")
            hrs_total=hrs_total+int(hrs_min[0])
            min_total=min_total+int(hrs_min[1])
            if int(hrs_min[1])>44:
                min_total_rnd=min_total_rnd+60
            elif (int(hrs_min[1])>30) and (int(hrs_min[1])<46):
                min_total_rnd=min_total_rnd+int(hrs_min[1])
            elif (int(hrs_min[1])>15) and (int(hrs_min[1])<31):
                min_total_rnd=min_total_rnd+30
            else:
                min_total_rnd=min_total_rnd+int(hrs_min[1])

total_time=str(int(hrs_total+((min_total-(min_total%60))/60)))+" hrs "+str(int(min_total%60))+" mins"
total_time_rnd=str(int(hrs_total+((min_total_rnd-(min_total_rnd%60))/60)))+" hrs "+str(int(min_total_rnd%60))+" mins"

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root=customtkinter.CTk()
root.geometry("340x500")
root.title("Nova's Classes")
#root.iconbitmap(resource_path("chaosicon.ico"))
root.resizable(False,False)

root.overrideredirect(True)
root.wm_attributes('-transparentcolor',"black")
colour="gray35"
colour1="gray20"

frame=customtkinter.CTkFrame(root, fg_color=colour1,bg_color="black",corner_radius=8)
frame.pack(pady=0,padx=0,fill="both",expand=True)

frame1=customtkinter.CTkFrame(frame, height=40,fg_color=colour,bg_color=colour1,corner_radius=8)
frame1.pack(pady=(5,0),padx=5,fill="both",expand=True)

label_1 = customtkinter.CTkLabel(frame1,text="UTILITIES" ,font=('Arial', 20,"bold"))
label_1.pack(pady=(8,0), padx=0)

buttonmove = customtkinter.CTkButton(frame1, hover=True, hover_color="lime green", width=33, height=23, fg_color=colour1,bg_color=colour, text="◎", text_color= colour, font=('Arial', 14,"bold"), corner_radius=8)
buttonmove.place(relx=0.03, rely=0.23)

def moveMouseButton(e):
   root.geometry(f'+{e.x_root}+{e.y_root}')

buttonmove.bind("<B1-Motion>", moveMouseButton)

buttonexit = customtkinter.CTkButton(frame1, hover=True, hover_color="red", width=33, height=23, fg_color=colour1,bg_color=colour, text="X", text_color= colour,font=('Arial', 12,"bold"), corner_radius=8, command=root.quit)
buttonexit.place(relx=0.873, rely=0.23)

frame1=customtkinter.CTkFrame(frame,height=50, fg_color=colour,bg_color=colour1,corner_radius=8)
frame1.pack(pady=(5,4),padx=5,fill="both",expand=True)

label_1 = customtkinter.CTkLabel(frame1,text="From: "+data[1]["date"]+" To: "+data[-1]["date"] ,font=('Arial', 16,"bold"))
label_1.pack(pady=(14,5), padx=0)
label_1 = customtkinter.CTkLabel(frame1,text="Total classes: "+str(total) ,font=('Arial', 16,"bold"))
label_1.pack(pady=(0,5), padx=0)
label_1 = customtkinter.CTkLabel(frame1,text="Total time: "+total_time ,font=('Arial', 16,"bold"))
label_1.pack(pady=(0,5), padx=0)
label_1 = customtkinter.CTkLabel(frame1,text="Total time rounded: "+total_time_rnd,font=('Arial', 16,"bold"))
label_1.pack(pady=(0,10), padx=0)

frame_list=customtkinter.CTkFrame(frame,height=100, fg_color=colour,bg_color=colour1,corner_radius=8)
frame_list.pack(pady=(0,6),padx=5,fill="both",expand=True)

label_1 = customtkinter.CTkLabel(frame_list,text="     Date                No. of Classes" ,font=('Arial', 16,"bold"))
label_1.pack(pady=(5,6), padx=0)

data_textbox = customtkinter.CTkTextbox(frame_list, width= 280,height=165,fg_color=colour1,bg_color=colour, corner_radius=8, font=('Arial', 14,"bold"), wrap="word",activate_scrollbars=False)
data_textbox.pack(pady=(0,10), padx=0)

for n in range(len(data)-1):
    sub_total=0
    for m in range(len(data[n+1]["classes"])):
        chk=data[n+1]["classes"][m]["cond"]
        if chk == "Y":
            sub_total=sub_total+1
    entry="    "+data[n+1]["date"]+"                        "+str(sub_total)+"\n\n"
    data_textbox.insert("1.0", entry)

data_textbox.configure(state="disabled")

ctk_textbox_scrollbar = customtkinter.CTkScrollbar(frame_list,fg_color=colour1,bg_color=colour, button_color=colour, corner_radius=8, height=152, command=data_textbox.yview)
ctk_textbox_scrollbar.place(relx=0.86, rely=0.194)

data_textbox.configure(yscrollcommand=ctk_textbox_scrollbar.set)

def create_spread():
    import excel_creator
    pass

frame1=customtkinter.CTkFrame(frame, height=40,fg_color=colour,bg_color=colour1,corner_radius=8)
frame1.pack(pady=(0,5),padx=5,fill="both",expand=True)

buttonsaveexcel = customtkinter.CTkButton(frame1, hover=True, hover_color="lime green", width=316, height=40, fg_color="forest green",bg_color=colour, text="Create Spreadsheet", text_color= "gray90", font=('Arial', 14,"bold"), corner_radius=8, command=create_spread)
buttonsaveexcel.pack(pady=(7,0), padx=0)

root.mainloop()
