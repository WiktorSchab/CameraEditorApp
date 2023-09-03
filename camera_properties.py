import cv2 as cv
from PIL import Image, ImageTk


def camera_update(camera, label, root):
    """

    :param camera: camera object to take image
    :param label: name of tkinter obj, where image from camera will be displayed
    :param root: main tk object
    """
    ret, frame = camera.read()

    if ret:
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        frame = Image.fromarray(frame)
        frame = ImageTk.PhotoImage(image=frame)

        # Setting frame as image
        label.imgtk = frame
        label.configure(image=frame)

    # Refreshing image every 10ms
    root.after(10, camera_update, camera, label, root)