import numpy as np
import cv2 as cv
from PIL import Image, ImageTk


def camera_update(camera, label_list, root, camera_instance):
    """

    :param camera: camera object to take image
    :param label_list: list with names of tkinter objs, where image from camera will be displayed
    :param root: main tk object
    :param camera_instance: instance of CameraClass contains info about camera
    """
    ret, frame = camera.read()

    if ret:
        if camera_instance.active == 0:
            laplacian = cv.Laplacian(frame, cv.CV_64F)
            frame = np.uint8(laplacian)

        frame_display = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        frame_display = Image.fromarray(frame_display)
        frame_display = ImageTk.PhotoImage(image=frame_display)

        # Setting frame as image
        label = label_list[camera_instance.active]
        label.imgtk = frame_display
        label.configure(image=frame_display)

    # Refreshing image every 10ms
    root.after(10, camera_update, camera, label_list, root, camera_instance)