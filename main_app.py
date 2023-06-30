import subprocess
import sys
import tkinter as tk
from tkinter import ttk
# Ignore warnings
import warnings

warnings.filterwarnings("ignore")

# Model
import torch

model = torch.hub.load('yolov5'  # Use backend for yolov5 in this folder
                       , 'custom'  # to use model in this folder
                       , path='./model/yolov5.pt'  # the name of model is this folder ## HERE
                       , source='local'  # to use backend from this folder
                       , force_reload=True  # clear catch
                       , device='0'  # use GPU
                       )
model.conf = 0.25  # NMS confidence threshold
model.iou = 0.45  # IoU threshold
model.multi_label = False  # NMS multiple labels per box
model.max_det = 1000  # maximum number of detections per image

# RUN
import cv2  # import opencv library
from glob import glob
import re
import datetime
import os

object_detected = 0
elapsed_time_after_id = None
current_directory = os.path.dirname(os.path.abspath(__file__))
result_directory = ''


def censorship_process(path, save_directory):
    global object_detected
    image_name = re.split(r'[/\\]', path)[-1]
    frame = cv2.imread(path)
    result = model(frame, size=416)
    coordinates = result.pandas().xyxy[0].to_dict(orient="records")

    for coordinate in coordinates:
        object_detected += 1
        object_detected_counter(object_detected)
        x1 = int(coordinate['xmin'])
        y1 = int(coordinate['ymin'])
        x2 = int(coordinate['xmax'])
        y2 = int(coordinate['ymax'])

        imgCrop = frame[y1:y2, x1:x2]
        imgBlur = cv2.blur(imgCrop, (50, 50))
        frame[y1:y2, x1:x2] = imgBlur

    write_status = cv2.imwrite(save_directory + '/' + image_name, frame)
    if write_status:
        print(image_name, 'written')
    else:
        print('problem')


# Function
from tkinter.filedialog import askdirectory, askopenfilenames
from tkinter import messagebox


# File mode
def files_censorship(files):
    global object_detected
    global result_directory
    object_detected = 0
    totalImage = len(files)
    counter = 0
    if totalImage:
        start_elapsed_time()
        new_dir_name = datetime.datetime.now().strftime("%S%M%H%d%m%Y")
        result_directory = current_directory + "\\result\\" + new_dir_name
        os.mkdir(result_directory)
        for file in files:
            censorship_process(file, result_directory)
            counter += 1
            scanned_image_counter(counter, totalImage)
        stop_elapsed_time()
        ask_open_folder()


# Directory mode
def batch_mode_censorship(directory):
    files = glob(directory + '/' + '*.jpg') + glob(directory + '/' + '*.png')
    files_censorship(files)


def select_directory():
    selected_folder = askdirectory()
    batch_mode_censorship(selected_folder)


def select_files():
    selected_files = askopenfilenames(
        title="Pilih File",
        filetypes=[("Image Files", (".jpg", ".png"))]
    )
    files_censorship(selected_files)


def update_elapsed_time(start_time):
    current_time = datetime.datetime.now()
    elapsed_time = current_time - start_time
    elapsed_time_str = str(elapsed_time).split('.')[0]  # Menghapus fraksi detik
    elapsed_time_value.config(text=elapsed_time_str)
    global elapsed_time_after_id
    elapsed_time_after_id = elapsed_time_value.after(1000, update_elapsed_time,
                                                     start_time)  # Memperbarui setiap 1 detik


def ask_open_folder():
    if messagebox.askyesno("Lihat Hasil", "Scan Finished\n"
                                          "Total Picture Scanned: {}\n"
                                          "Object Found: {}\n"
                                          "Elapsed Time: {}\n"
                                          "Apakah anda ingin melihat hasilnya ?".format(
        total_picture_scanned_value.cget('text'),
        object_found_value.cget('text'),
        elapsed_time_value.cget('text'))):
        subprocess.Popen(r'explorer /open, "{}"'.format(result_directory))


def stop_elapsed_time():
    elapsed_time_value.after_cancel(elapsed_time_after_id)


def start_elapsed_time():
    start_time = datetime.datetime.now()
    update_elapsed_time(start_time)


def on_closing(window):
    if messagebox.askokcancel("Konfirmasi", "Apakah Anda ingin menutup aplikasi?"):
        window.destroy()
        sys.exit()


def scanned_image_counter(counter, total_image):
    total_picture_scanned_value.configure(text="{}/{}".format(counter, total_image))
    window.update()


def object_detected_counter(counter):
    object_found_value.configure(text=counter)
    window.update()


# Graphical User Interface

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
tombol_batch.pack(padx=10, pady=10)

# Tombol pilih file
tombol_single = ttk.Button(input_container_frame, text="Select File", command=select_files)
tombol_single.pack(padx=10, pady=10)

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

# Close Program
window.protocol("WM_DELETE_WINDOW", lambda: on_closing(window))

window.mainloop()
