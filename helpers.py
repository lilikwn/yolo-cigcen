from tkinter.filedialog import askdirectory, askopenfilenames
import sys
import censorship_process
from datetime import datetime
from tkinter import messagebox

def select_directory():
    selected_folder = askdirectory()
    print(selected_folder)
    censorship_process.batch_mode_censorship(selected_folder)

def select_files():
    selected_files = askopenfilenames(
        title="Pilih File",
        filetypes=[("Image Files", (".jpg", ".png"))]
    )
    print(type(selected_files))
    censorship_process.files_censorship(selected_files)

def update_elapsed_time(start_time,label):
    current_time = datetime.now()
    elapsed_time = current_time - start_time
    elapsed_time_str = str(elapsed_time).split('.')[0]  # Menghapus fraksi detik
    label.config(text=elapsed_time_str)
    label.after(1000, update_elapsed_time)  # Memperbarui setiap 1 detik

def on_closing(window):
    if messagebox.askokcancel("Konfirmasi", "Apakah Anda ingin menutup aplikasi?"):
        window.destroy()
        sys.exit()
