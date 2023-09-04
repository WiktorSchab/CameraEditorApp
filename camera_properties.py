import numpy as np
import cv2 as cv
from PIL import Image, ImageTk

import pyvirtualcam


def camera_update(camera, label_list, camera_instance):
    """

    :param camera: camera object to take image
    :param label_list: list with names of tkinter objs, where image from camera will be displayed
    :param camera_instance: instance of CameraClass contains info about camera
    """

    # Get the width and height of the video frames
    frame_width = int(camera.get(3))
    frame_height = int(camera.get(4))

    # Create a pyvirtualcam camera
    with pyvirtualcam.Camera(width=frame_width, height=frame_height, fps=30) as cam:
        while True:
            ret, frame = camera.read()  # Read a frame from the video

            # Applying filter
            laplacian = cv.Laplacian(frame, cv.CV_64F)
            filter_frame = np.uint8(laplacian)

            # If active Tab is Tab nr 0
            if camera_instance.active == 0:
                # frame is image that is displaying in tkinter
                frame = filter_frame

            # Converting img to display
            frame_display = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            frame_display = Image.fromarray(frame_display)
            frame_display = ImageTk.PhotoImage(image=frame_display)

            # Setting frame as image
            label = label_list[camera_instance.active]
            label.imgtk = frame_display
            label.configure(image=frame_display)

            if not ret:
                break

            # Resize the frame
            frame_resized = cv.resize(filter_frame, (frame_width, frame_height))

            # Send the frame to the virtual camera
            cam.send(frame_resized)
            cam.sleep_until_next_frame()
