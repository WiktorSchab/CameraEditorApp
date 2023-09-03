import numpy as np
import cv2 as cv
from PIL import Image, ImageTk

import pyvirtualcam

def camera_update(camera, label_list, root, camera_instance):
    """

    :param camera: camera object to take image
    :param label_list: list with names of tkinter objs, where image from camera will be displayed
    :param root: main tk object
    :param camera_instance: instance of CameraClass contains info about camera
    """

    cap = cv.VideoCapture(0)
    # Get the width and height of the video frames
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    # Create a pyvirtualcam camera
    with pyvirtualcam.Camera(width=frame_width, height=frame_height, fps=30) as cam:
        while True:
            ret, frame = cap.read()  # Read a frame from the video

            # Applying filter
            laplacian = cv.Laplacian(frame, cv.CV_64F)
            frame = np.uint8(laplacian)

            #
            frame_display = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            frame_display = Image.fromarray(frame_display)
            frame_display = ImageTk.PhotoImage(image=frame_display)

            # Setting frame as image
            label = label_list[camera_instance.active]
            label.imgtk = frame_display
            label.configure(image=frame_display)

            if not ret:
                break

            frame_resized = cv.resize(frame, (frame_width, frame_height))  # Resize the frame

            cam.send(frame_resized)  # Send the frame to the virtual camera
            cam.sleep_until_next_frame()

    ret, frame = camera.read()

    if ret:
        # if Tab 0 (modified) is active
        if camera_instance.active == 0:
            # Applying filter
            laplacian = cv.Laplacian(frame, cv.CV_64F)
            frame = np.uint8(laplacian)

            # Getting width and height of camera obj
            frame_width = int(camera.get(3))
            frame_height = int(camera.get(4))

            with pyvirtualcam.Camera(width=frame_width, height=frame_height, fps=30) as cam:
                frame_resized = cv.resize(frame, (frame_width, frame_height))

                # Sending image to virtual camera
                cam.send(frame_resized)
                cam.sleep_until_next_frame()

        frame_display = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        frame_display = Image.fromarray(frame_display)
        frame_display = ImageTk.PhotoImage(image=frame_display)



    # Refreshing image every 10ms
    root.after(1, camera_update, camera, label_list, root, camera_instance)