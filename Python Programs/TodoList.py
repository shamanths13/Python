import customtkinter
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root=customtkinter.CTk()
root.geometry("400x600")
root.title("Nova's ToDo List")
root.resizable(False,False)

def buttonfunc():
    print("Test")

check_box_list = []

def addCheckBox():
    checkBoxName = str.capitalize(entry.get())
    entry.delete(0,100)
    c = customtkinter.CTkCheckBox(bframe, text=checkBoxName,font=('Arial', 16,"bold"),height=30, width=450)
    c.pack(pady=2, padx=10)
    check_box_list.append(c)

def del_entry():
    i=check_box_list[-1]
    i.destroy()
    check_box_list.pop()

def clear():
    for i in check_box_list:
        i.destroy()

def clr_sel():
    pass
frame=customtkinter.CTkFrame(root,fg_color="dark slate blue")
frame.pack(pady=0,padx=0,fill="both",expand=True)

#label=customtkinter.CTkLabel(frame, text="Nova's ToDo List", font=('Arial', 28,"bold"), text_color="dark turquoise")
#label.pack(pady=10, padx=0)

entry = customtkinter.CTkEntry(master=frame,width=256,height=36,corner_radius=8,font=('Arial', 20,"bold"))
entry.pack(pady=10, padx=(0,123))

button = customtkinter.CTkButton(master=frame, hover=True, hover_color="green", width=50, height=36, fg_color="grey", text="ADD",font=('Arial', 12,"bold"), corner_radius=8, command=addCheckBox)
button.place(relx=0.756, rely=0.05, anchor=customtkinter.CENTER)

button = customtkinter.CTkButton(master=frame, hover=True, hover_color="maroon", width=50, height=36, fg_color="grey", text="DEL",font=('Arial', 12,"bold"), corner_radius=8, command=del_entry)
button.place(relx=0.91, rely=0.05, anchor=customtkinter.CENTER)

bframe=customtkinter.CTkFrame(frame, height=35, width=450,fg_color="dark slate blue")
bframe.pack(pady=0, padx=10,anchor="w")

button = customtkinter.CTkButton(master=frame, hover=True, hover_color="maroon", width=100, height=36, fg_color="grey", text="clr slect",font=('Arial', 12,"bold"), corner_radius=8, command=clr_sel)
button.place(relx=0.27, rely=0.95, anchor=customtkinter.CENTER)

button = customtkinter.CTkButton(master=frame, hover=True, hover_color="maroon", width=100, height=36, fg_color="grey", text="CLEAR",font=('Arial', 12,"bold"), corner_radius=8, command=clear)
button.place(relx=0.5, rely=0.95, anchor=customtkinter.CENTER)

button = customtkinter.CTkButton(master=frame, hover=True, hover_color="maroon", width=100, height=36, fg_color="grey", text="EXIT",font=('Arial', 12,"bold"), corner_radius=8, command=root.quit)
button.place(relx=0.73, rely=0.95, anchor=customtkinter.CENTER)

root.mainloop()