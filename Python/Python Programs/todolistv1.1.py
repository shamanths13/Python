import customtkinter
import os, sys
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

def resource_path(relative_path):
    try:
        base_path=sys._MEIPASS
    except Exception:
        base_path=os.path.abspath(".")
    return os.path.join(base_path, relative_path)

root=customtkinter.CTk()
root.geometry("400x600")
root.title("Nova's ToDo List")
#root.iconbitmap(resource_path("chaosicon.ico"))
root.resizable(False,False)

def buttonfunc():
    print("Test")

check_box_list = []

def addCheckBox():
    checkBoxName = str.capitalize(entry.get())
    if checkBoxName=="":
        return
    entry.delete(0,100)
    c = customtkinter.CTkCheckBox(bframe, text=checkBoxName,font=('Arial', 16,"bold"),height=30, width=450,fg_color="olive drab",hover_color="dark olive green4")
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
    for i in check_box_list:
        val=i.get()
        if val==1:
            i.destroy()

colour="gray30"
colour1="gray20"
frame=customtkinter.CTkFrame(root,fg_color=colour,bg_color=colour)
frame.pack(pady=0,padx=0,fill="both",expand=True)

entry = customtkinter.CTkEntry(master=frame,width=380,height=36,corner_radius=8,font=('Arial', 20,"bold"),fg_color=colour1)
entry.pack(pady=10, padx=0)

button = customtkinter.CTkButton(master=frame, hover=True, hover_color="dark olive green", width=33, height=20, bg_color=colour1, fg_color=colour1, text="+",font=('Arial', 18,"bold"), corner_radius=6, command=addCheckBox)
button.place(relx=0.923, rely=0.046, anchor=customtkinter.CENTER)

bframe=customtkinter.CTkFrame(frame, height=35, width=450,fg_color=colour)
bframe.pack(pady=0, padx=10,anchor="w")

button = customtkinter.CTkButton(master=frame, hover=True, hover_color="olive drab", width=100, height=32, fg_color=colour, text="CLR SEL",font=('Arial', 12,"bold"), corner_radius=8, command=clr_sel)
button.place(relx=0.20, rely=0.96, anchor=customtkinter.CENTER)

button = customtkinter.CTkButton(master=frame, hover=True, hover_color="orangered3", width=100, height=32, fg_color=colour, text="CLR ALL",font=('Arial', 12,"bold"), corner_radius=8, command=clear)
button.place(relx=0.5, rely=0.96, anchor=customtkinter.CENTER)

button = customtkinter.CTkButton(master=frame, hover=True, hover_color="maroon", width=100, height=32, fg_color=colour, text="EXIT",font=('Arial', 12,"bold"), corner_radius=8, command=root.quit)
button.place(relx=0.80, rely=0.96, anchor=customtkinter.CENTER)

root.mainloop()