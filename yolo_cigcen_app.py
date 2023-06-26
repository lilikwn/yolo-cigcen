import sys
import tkinter as tk
from tkinter import ttk, Label
from helpers import on_closing, select_directory, select_files

def scanned_image_counter(counter, total_image):
    total_picture_scanned_value.configure(text="{}/{}".format(counter, total_image))
    window.update()

# Main Window
window = tk.Tk()
window.title("Yolo-CigCen")
window.geometry("640x480")
window.resizable(False, False)

# Style
style1 = ttk.Style()
style1.configure('Style1.TFrame', background='#FAFAFA')
style2 = ttk.Style()
style2.configure('Style2.TFrame', background='#606A85')

# Frame Input PATH
input_frame = ttk.Frame(window)
# Penempatan
input_frame.pack()
input_frame.pack_propagate(False)
input_frame.configure(borderwidth=1, relief='solid', style='Style1.TFrame', width=640, height=180)

# Button Input Container
input_container_frame = ttk.Frame(input_frame)
input_container_frame.place(relx=.5, rely=.5, anchor="c")
input_container_frame.configure(style="Style1.TFrame")

# Info Frame
info_frame = ttk.Frame(window)
# Penempatan
info_frame.pack()
info_frame.pack_propagate(False)
info_frame.configure(borderwidth=1, relief='solid', style='Style2.TFrame', width=640, height=300)

# Status Frame
status_frame = ttk.Frame(info_frame)
status_frame.place(relx=.5, rely=.5, anchor="c")
status_frame.configure(style="Style2.TFrame")

# Tombol
explorer = tk.Tk()
explorer.withdraw()

tombol_batch = ttk.Button(input_container_frame, text="Open Directory", command=select_directory)
tombol_batch.pack(padx=10,pady=10)

# Tombol pilih file
tombol_single = ttk.Button(input_container_frame, text="Select File", command=select_files)
tombol_single.pack(padx=10,pady=10)

# Frame Info Label Style
style_label_info = ttk.Style()
style_label_info.configure('Custom.TLabel',
                           background='#606A85',
                           foreground='white',
                           font=("Arial", 14))

# Value of Frame Info
# Total Pictures Scanned
total_picture_scanned_label = ttk.Label(status_frame, text="Total Pictures Scanned:", style='Custom.TLabel')
total_picture_scanned_label.grid(row=0, column=0, sticky='e', pady=10, padx=10)

total_picture_scanned_value = ttk.Label(status_frame, text="0/0", style='Custom.TLabel')
total_picture_scanned_value.grid(row=0, column=1, sticky='w', pady=10, padx=10)

# Object Found
object_found_label = ttk.Label(status_frame, text="Object Found:", style='Custom.TLabel')
object_found_label.grid(row=1, column=0, sticky='e', pady=10, padx=10)

object_found_value = ttk.Label(status_frame, text="0", style='Custom.TLabel')
object_found_value.grid(row=1, column=1, sticky='w', pady=10, padx=10)

# Elapsed time
elapsed_time_label = ttk.Label(status_frame, text="Elapsed Time:", style='Custom.TLabel')
elapsed_time_label.grid(row=2, column=0, sticky='e', pady=10, padx=10)

elapsed_time_value = ttk.Label(status_frame, text="00:00:00", style='Custom.TLabel')
elapsed_time_value.grid(row=2, column=1, sticky='w', pady=10, padx=10)

# start_time = datetime.now()
# update_elapsed_time()

# Close Program
window.protocol("WM_DELETE_WINDOW", lambda: on_closing(window))

window.mainloop()