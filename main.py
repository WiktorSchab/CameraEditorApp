import os
import tkinter as tk
from tkinter import ttk

import cv2 as cv
import pyvirtualcam
from PIL import Image, ImageTk

from camera_class import CameraClass

# Setting instance with tab 0 as active one
camera_instance = CameraClass(0)

def camera_update():
    ret, frame = camera.read()

    if ret:
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        frame = Image.fromarray(frame)
        frame = ImageTk.PhotoImage(image=frame)

        # Setting frame as image
        original_camera.imgtk = frame
        original_camera.configure(image=frame)

    # Setting refreshing ratio in ms
    root.after(10, camera_update)


def current_camera(*args):
    tab_num = str(main_camera_tab.index(main_camera_tab.select()))
    camera_instance.active = tab_num
    print(camera_instance.active)


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
main_camera_tab = ttk.Notebook(main_frame)
main_camera_tab.grid(row=0, column=1)

# Modified image from camera | Tab 0
modified_camera = tk.Label(main_camera_tab, text='In progress')
modified_camera.grid(row=0, column=0)

# Original image from camera | Tab 1
original_camera = tk.Label(main_camera_tab)
original_camera.grid(row=0, column=0)

# Tabs with camera
main_camera_tab.add(modified_camera, text='Modified camera')
main_camera_tab.add(original_camera, text='Original camera')
main_camera_tab.bind('<<NotebookTabChanged>>', current_camera)

main_frame.pack(fill='x')

camera_update()

root.mainloop()
# After closing window
camera.release()
