def scanned_image_counter(counter, total_image):
    import yolo_cigcen_app
    yolo_cigcen_app.total_picture_scanned_value.configure(text="{}/{}".format(counter, total_image))
    yolo_cigcen_app.window.update()