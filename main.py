import os
import tkinter as tk

import cv2 as cv
import pyvirtualcam
from PIL import Image, ImageTk


def camera_update():
    ret, frame = camera.read()

    if ret:
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        frame = Image.fromarray(frame)
        frame = ImageTk.PhotoImage(image=frame)

        # Setting frame as image
        center.imgtk = frame
        center.configure(image=frame)

    # Setting refreshing ratio in ms
    root.after(10, camera_update)


root = tk.Tk()

# Configuration of window
root.geometry('900x600')
root.title('Camera Editor App')
root.resizable(False, False)

camera = cv.VideoCapture(0)

# Content will all
main_frame = tk.Frame(root)

# Amount of columns
main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=1)
main_frame.columnconfigure(2, weight=1)

# Left side
left_side = tk.Button(main_frame, text='1')
left_side.grid(row=0, column=0)

# Center of window
center = tk.Label(main_frame)
center.grid(row=0, column=1)

main_frame.pack(fill='x')


camera_update()

root.mainloop()
# After closing window
camera.release()
