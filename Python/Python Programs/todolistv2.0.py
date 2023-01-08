import customtkinter
import tkinter as ttk
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root=customtkinter.CTk()
root.geometry("400x600")
root.title("To Do List")
#root.iconbitmap(resource_path("chaosicon.ico"))
root.resizable(False,False)

root.overrideredirect(True)
root.wm_attributes('-transparentcolor',"black")
colour="gray30"
colour1="gray20"


def createtab():
    name=str.capitalize(entrytab.get())
    entrytab.delete(0,100)
    tab=tabview.insert(0,name)
    tab.grid_columnconfigure(0, weight=1)
    tabview.set(name)

    check_box_list = []
    global colvar
    def checkboxlimit():
        if len(check_box_list)<12:
            addCheckBox()
        else:
            pass


    def addCheckBox():
        checkBoxName = str.capitalize(entry.get())
        if checkBoxName=="":
            return
        entry.delete(0,100)
        c = customtkinter.CTkCheckBox(frame2, text=checkBoxName,font=('Arial', 16,"bold"),height=30, width=360,fg_color="olive drab",hover_color="dark olive green4")
        c.pack(pady=(0,4), padx=10)
        check_box_list.append(c)

    def deletelist():
        name=tabview.get()
        tabview.delete(name)
        tabview.set("+")

    def clear():
        tempchkboxlist=len(check_box_list)
        for i in range(tempchkboxlist):
            check_box_list[i].destroy()

        for i in range(tempchkboxlist):

            check_box_list.pop()

    def clr_sel():
        templist=[]
        for i in check_box_list:
            val=i.get()
            if val==1:
                i.destroy()
                templist.append(i)
        for i in templist:
            check_box_list.remove(i)

    

    entry = customtkinter.CTkEntry(tab,width=380,height=36,corner_radius=8,font=('Arial', 20,"bold"),fg_color=colour1, placeholder_text_color="gray30", placeholder_text="Add item")
    entry.pack(pady=0,padx=0)

    frame2=customtkinter.CTkFrame(tab,fg_color=tabcolourslist[colvar], height=300)
    frame2.pack(pady=10,padx=0,fill="both",expand=True)

    label_1 = customtkinter.CTkLabel(frame2,text=str.upper(name) ,font=('Arial', 20,"bold"))
    label_1.pack(pady=(7,3), padx=0)

    frame1=customtkinter.CTkFrame(tab,fg_color=colour1, height=20)
    frame1.pack(pady=10,padx=0,fill="both",expand=False)

    button = customtkinter.CTkButton(tab, hover=True, hover_color="dark olive green", width=33, height=20, bg_color=colour1, fg_color=colour1, text="+",font=('Arial', 18,"bold"), corner_radius=6, command=checkboxlimit)
    button.place(relx=0.945, rely=0.034, anchor=customtkinter.CENTER)

    button = customtkinter.CTkButton(tab, hover=True, hover_color="olive drab", width=100, height=32, fg_color=colour, text="CLR SEL",font=('Arial', 12,"bold"), corner_radius=8, command=clr_sel)
    button.place(relx=0.20, rely=0.965, anchor=customtkinter.CENTER)

    button = customtkinter.CTkButton(tab, hover=True, hover_color="orangered3", width=100, height=32, fg_color=colour, text="CLR ALL",font=('Arial', 12,"bold"), corner_radius=8, command=clear)
    button.place(relx=0.5, rely=0.965, anchor=customtkinter.CENTER)

    button = customtkinter.CTkButton(tab, hover=True, hover_color="maroon", width=100, height=32, fg_color=colour, text="DEL LIST",font=('Arial', 12,"bold"), corner_radius=8, command=deletelist)
    button.place(relx=0.80, rely=0.965, anchor=customtkinter.CENTER)


def moveMouseButton(e):
   root.geometry(f'+{e.x_root}+{e.y_root}')
    

frame=customtkinter.CTkFrame(root,fg_color="black")
frame.pack(pady=0,padx=0,fill="both",expand=True)

tabview = customtkinter.CTkTabview(frame, width=400,height=600, corner_radius=10,fg_color= colour1, segmented_button_selected_color="dark olive green")
tabview.grid(row=0, padx=0, pady=00)
tab1=tabview.add("+")
tab1.grid_columnconfigure(0, weight=1)

label_1 = customtkinter.CTkLabel(tab1,text="NOVA'S TO DO LIST" ,font=('Arial', 22,"bold"))
label_1.pack(pady=(0,10), padx=0)

entrytab = customtkinter.CTkEntry(tab1,width=360,height=36,corner_radius=8,font=('Arial', 20,"bold"),fg_color=colour1,placeholder_text_color="gray30", placeholder_text="Enter a new list name here")
entrytab.pack(padx=0, pady=0)

tabcolourslist=["MediumPurple4","skyblue4","Dark Slate gray","gray30"]
tabhvrcolourslist=["MediumPurple2","skyblue2","Slate gray","gray40"]
colvar=3

def col0():
    global colvar
    colvar=0
    createtab()

def col1():
    global colvar
    colvar=1
    createtab()

def col2():
    global colvar
    colvar=2
    createtab()

def col3():
    global colvar
    colvar=3
    createtab()


buttoncol = customtkinter.CTkButton(tab1, hover=True, hover_color=tabhvrcolourslist[0], width=70, height=40, bg_color=colour1, fg_color=tabcolourslist[0], text="+",font=('Arial', 20,"bold"), corner_radius=6, command=col0)
buttoncol.place(relx=0.12, rely=0.2, anchor=customtkinter.CENTER)

buttoncol = customtkinter.CTkButton(tab1, hover=True, hover_color=tabhvrcolourslist[1], width=70, height=40, bg_color=colour1, fg_color=tabcolourslist[1], text="+",font=('Arial', 18,"bold"), corner_radius=6, command=col1)
buttoncol.place(relx=0.3733, rely=0.2, anchor=customtkinter.CENTER)

buttoncol = customtkinter.CTkButton(tab1, hover=True, hover_color=tabhvrcolourslist[2], width=70, height=40, bg_color=colour1, fg_color=tabcolourslist[2], text="+",font=('Arial', 18,"bold"), corner_radius=6, command=col2)
buttoncol.place(relx=0.6266, rely=0.2, anchor=customtkinter.CENTER)

buttoncol = customtkinter.CTkButton(tab1, hover=True, hover_color=tabhvrcolourslist[3], width=70, height=40, bg_color=colour1, fg_color=tabcolourslist[3], text="+",font=('Arial', 18,"bold"), corner_radius=6, command=col3)
buttoncol.place(relx=0.88, rely=0.2, anchor=customtkinter.CENTER)

buttonexit = customtkinter.CTkButton(root, hover=True, hover_color="orangered3", width=33, height=23, fg_color=colour1,bg_color=colour1, text="X", text_color= colour1,font=('Arial', 12,"bold"), corner_radius=8, command=root.quit)
buttonexit.place(relx=0.952, rely=0.053, anchor=customtkinter.CENTER)

buttonmove = customtkinter.CTkButton(root, hover=True, hover_color="dark olive green", width=33, height=23, fg_color=colour1,bg_color=colour1, text="◎", text_color= colour1, font=('Arial', 14,"bold"), corner_radius=8)
buttonmove.place(relx=0.048, rely=0.053, anchor=customtkinter.CENTER)

buttonmove.bind("<B1-Motion>", moveMouseButton)

switch_var = customtkinter.StringVar(value="on")
root.wm_attributes('-topmost', True)

def switch_event():
    switch_state=switch_var.get()
    if switch_state == "on":
        root.wm_attributes('-topmost', True)
    else:
        root.wm_attributes('-topmost', False)


switch_1 = customtkinter.CTkSwitch(master=tab1, text="Always on Top",font=('Arial', 14,"bold"), command=switch_event,variable=switch_var, onvalue="on", offvalue="off")
switch_1.place(relx=0.2, rely=0.3, anchor=customtkinter.CENTER)


label_1 = customtkinter.CTkLabel(tab1,text="NOTES" ,font=('Arial', 20,"bold"))
label_1.place(relx=0.5, rely=0.37, anchor=customtkinter.CENTER)

textbox = customtkinter.CTkTextbox(tab1, width=360, height=307, fg_color=colour, corner_radius=10,font=('Arial', 14,"bold"), wrap="word")
textbox.place(relx=0.5, rely=0.7, anchor=customtkinter.CENTER)

textbox.insert("0.0", "Instructions: ")
textbox.insert("1.0", "") 
textbox.insert("2.0", "Click the upper right corner to exit. ") 
textbox.insert("3.0", "Click and drag the upper left corner to move the pad. ")
textbox.insert("4.0", "Enter name of the list and choose a colour to create a new list. The name of the list should be uinque. ")
textbox.insert("5.0", "Type any non list notes here. ")
text = textbox.get("0.0", "end")

textbox.configure(state="normal") 

def cleartxt():
    textbox.delete("0.0","1000.0")

button = customtkinter.CTkButton(tab1, hover=True, hover_color="orangered3", width=0, height=10, fg_color=colour,bg_color=colour, text="Clear",font=('Arial', 12,"bold"), corner_radius=8, command=cleartxt)
button.place(relx=0.5, rely=0.945, anchor=customtkinter.CENTER)

root.mainloop()