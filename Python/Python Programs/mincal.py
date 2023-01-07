from tkinter import *
from tkinter import ttk

# Create main window
main = Tk()
main.title('Currency Converter')
main.geometry("300x230")

# Create Tab
my_converter = ttk.Notebook(main)
my_converter.pack(pady=5)

# Create Frames
converter_frame = Frame(my_converter, width=300, height=200)

# Add our Tabs
my_converter.add(converter_frame, text="INR to EUR Converter")

# Create INR Frame
inr_frame = LabelFrame(converter_frame, text="Enter INR", font=("Helvetica", 10))
inr_frame.pack(pady=5)

# Create INR entry box
inr_entry = Entry(inr_frame, font=("Helvetica", 18))
inr_entry.pack(pady=0, padx=10)

# Create Eur Frame
eur_label = LabelFrame(converter_frame, text="Converted Currency in EUR", font=("Helvetica", 10))
eur_label.pack(pady=5, padx=5)

# Create EUR Box
eur_entry = Entry(eur_label, font=("Helvetica", 18))
eur_entry.pack(pady=10, padx=10)

# Create convert command
def convert():
	# Clear EUR Box
    eur_entry.delete(0, END)
	# Convert
    conversion = float(inr_entry.get()) * 0.011
	# Round to two decimals
    conversion = round(conversion,2)
	# Convert to string
    conversion=str(conversion)
	# Add Dollar Sign
    conversion= " € "+ conversion
	# Insert in EUR Box
    eur_entry.insert(0, conversion)	

# Create Convert Button
convert_button = Button(inr_frame, text="Convert", command=convert)
convert_button.pack(pady=10)

main.mainloop()

