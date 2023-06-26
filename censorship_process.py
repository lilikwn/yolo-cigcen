# Ignore warnings
import warnings
warnings.filterwarnings("ignore") # Warning will make operation confuse!!!

# Model
import torch
model = torch.hub.load(   'yolov5' # Use backend for yolov5 in this folder
                        , 'custom' # to use model in this folder
                        , path='./model/yolov5.pt' # the name of model is this folder ## HERE
                        , source='local' # to use backend from this folder
                        , force_reload=True # clear catch
                        , device = '0' # I want to use CPU
                    )
model.conf = 0.25 # NMS confidence threshold
model.iou = 0.45  # IoU threshold
model.multi_label = False  # NMS multiple labels per box
model.max_det = 1000  # maximum number of detections per image

# RUN
import cv2 #import opencv library
from glob import glob
import re
import datetime
import os
# import yolo_cigcen_app
# image_dir = '' #import image
# directory = './random_data/'
# files = glob(directory+'*.jpg') + glob(directory + '*.png')

# print(files)

def censorship_process(path, save_directory):
    image_name = re.split(r'[/\\]', path)[-1]
    print(image_name)
    frame = cv2.imread(path)
    width = int(frame.shape[1] * 0.4)
    height = int(frame.shape[0] * 0.4)
    result = model(frame, size=416)
    coordinates = result.pandas().xyxy[0].to_dict(orient="records")

    for coordinate in coordinates:
        con = coordinate['confidence']
        cs = coordinate['class']

        x1 = int(coordinate['xmin'])
        y1 = int(coordinate['ymin'])
        x2 = int(coordinate['xmax'])
        y2 = int(coordinate['ymax'])

        imgCrop = frame[y1:y2, x1:x2]
        imgBlur = cv2.blur(imgCrop, (50, 50))
        frame[y1:y2, x1:x2] = imgBlur

        print(x1, y1, x2, y2)
    write_status = cv2.imwrite(save_directory + '/' + image_name, frame)
    if write_status:
        print(image_name, 'written')
    else:
        print('problem')
    # resize = cv2.resize(frame, (width, height))
    # cv2.imshow('Object Detector', resize)
    # cv2.waitKey(0)

# Directory mode
def batch_mode_censorship(directory):
    from counter_helpers import scanned_image_counter
    files = glob(directory + '/' + '*.jpg') + glob(directory + '/' + '*.png')
    new_dir_name = datetime.datetime.now().strftime("%S%M%H%d%m%Y")
    totalImage = len(files)
    counter = 0
    print(new_dir_name)
    print(files)
    result_directory = './result/' + new_dir_name
    os.mkdir(result_directory)
    for file in files:
        censorship_process(file, result_directory)
        counter+=1
        scanned_image_counter(counter, totalImage)

# File mode
def files_censorship(files):
    from counter_helpers import scanned_image_counter
    new_dir_name = datetime.datetime.now().strftime("%S%M%H%d%m%Y")
    totalImage = len(files)
    counter = 0
    print(new_dir_name)
    result_directory = './result/' + new_dir_name
    os.mkdir(result_directory)
    for file in files:
        censorship_process(file, result_directory)
        counter += 1
        scanned_image_counter(counter, totalImage)
