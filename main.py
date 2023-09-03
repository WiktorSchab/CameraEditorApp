import os
import tkinter as tk
from tkinter import ttk, PhotoImage

import cv2 as cv
import pyvirtualcam

from camera_class import CameraClass
from camera_properties import camera_update


# Setting instance with tab 0 as active one
camera_instance = CameraClass(0)


def current_camera(*args):
    tab_num = int(main_camera_tab.index(main_camera_tab.select()))
    camera_instance.active = tab_num


root = tk.Tk()

# Configuration of window
root.geometry('900x600')
root.title('Camera Editor App')
root.resizable(False, False)


camera = cv.VideoCapture(0)

# Content will all
main_frame = tk.Frame(root)

bg = PhotoImage(file=r'graphic\bg.png')
bg_label = tk.Label(main_frame, image=bg)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

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

main_frame.pack(fill='both', expand=True)

# List of labels where to display cameras
label_list = [modified_camera, original_camera]
# Calling function to updating camera image
camera_update(camera, label_list, root, camera_instance)

root.mainloop()
# After closing window
camera.release()
