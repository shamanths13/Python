import os
import json
import customtkinter

with open(os.path.join(os.path.dirname(__file__),"classesdone_backup.json"), 'r') as f:
    data = json.load(f)

with open(os.path.join(os.path.dirname(__file__),"classesdone.json"), 'w') as x:
    json.dump(data, x, indent = 4)

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root=customtkinter.CTk()
root.geometry("260x95")
root.title("Nova's Classes")
#root.iconbitmap(resource_path("chaosicon.ico"))
root.resizable(False,False)

root.overrideredirect(True)
root.wm_attributes('-transparentcolor',"black")
colour="gray35"
colour1="gray20"

frame=customtkinter.CTkFrame(root, fg_color=colour1,bg_color="black",corner_radius=8)
frame.pack(pady=0,padx=0,fill="both",expand=True)

frame2=customtkinter.CTkFrame(frame, fg_color=colour,bg_color=colour1,corner_radius=8)
frame2.pack(pady=5,padx=5,fill="both",expand=True)

label_1 = customtkinter.CTkLabel(frame2,text="Back Up Restored!" ,font=('Arial', 20,"bold"))
label_1.pack(pady=(10,10), padx=0)

buttonexit = customtkinter.CTkButton(frame2, hover=True, hover_color="red", width=33, height=23, fg_color="red4",bg_color=colour, text="Ok", text_color= "gray80",font=('Arial', 12,"bold"), corner_radius=8, command=root.quit)
buttonexit.pack(pady=(0,10), padx=50)

root.mainloop()