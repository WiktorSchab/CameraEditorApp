import tkinter as tk
from tkinter import ttk, PhotoImage
import threading

import cv2 as cv

from camera.camera_class import CameraClass
from camera.camera_properties import camera_update
from settings.settings_gui import filters_setting, app_setting

# Setting instance with tab 0 as active one
camera_instance = CameraClass(0)


def hide_content(setting_number):
    if setting_number == 1:
        filters_setting(root, main_frame, camera_instance)
    elif setting_number == 2:
        app_setting(root, main_frame, camera_instance)


def show_content():
    main_frame.pack(fill='both', expand=True)


# Changing current tab number
def current_camera(event):
    tab_num = int(main_camera_tab.index(main_camera_tab.select()))
    camera_instance.active_window_number = tab_num


# Tread for updating camera image.
def start_camera_thread():
    camera_thread = threading.Thread(target=camera_update, args=(camera, label_list, camera_instance))
    camera_thread.daemon = True
    camera_thread.start()


# Selecting filter
def select_filter(event):
    w = event.widget
    index = int(w.curselection()[0])
    value = w.get(index)

    # Changing active filter
    camera_instance.active_filter = index
    print(value, index)


root = tk.Tk()

# Configuration of window
root.geometry('900x600')
root.title('Camera Editor App')
root.resizable(False, False)

my_menu = tk.Menu(root)
root.config(menu=my_menu)

# Camera device
camera = cv.VideoCapture(0)

# Sub-menu settings
settings = tk.Menu(my_menu)
settings.add_command(label='Filter Settings', command=lambda: hide_content(1))
settings.add_command(label='App Settings', command=lambda: hide_content(2))
my_menu.add_cascade(label='Settings', menu=settings)

# Content will all labels
main_frame = tk.Frame(root)

bg = PhotoImage(file=r'graphic\bg.png')
bg_label = tk.Label(main_frame, image=bg)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Amount of columns
main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=1)
main_frame.columnconfigure(2, weight=1)

main_frame.rowconfigure(0, weight=1)
main_frame.rowconfigure(1, weight=1)
main_frame.rowconfigure(2, weight=1)

# Left side
filter_list = ['Default', 'Gray', 'Laplacian', 'Blur', 'Bilateral']

my_listbox = tk.Listbox(main_frame)
my_listbox.grid(row=0, column=0)

for item in filter_list:
    my_listbox.insert('end', item)

my_listbox.bind('<<ListboxSelect>>', select_filter)

# Center of window
main_camera_tab = ttk.Notebook(main_frame)
main_camera_tab.grid(row=0, column=1)

# Modified image from camera | Tab 0
modified_camera = tk.Label(main_camera_tab)
modified_camera.grid(row=0, column=0)

# Original image from camera | Tab 1
original_camera = tk.Label(main_camera_tab)
original_camera.grid(row=0, column=0)

# List of labels where to display cameras
label_list = [modified_camera, original_camera]

# Tabs with camera
main_camera_tab.add(modified_camera, text='Modified camera')
main_camera_tab.add(original_camera, text='Original camera')
main_camera_tab.bind('<<NotebookTabChanged>>', current_camera)


main_frame.pack(fill='both', expand=True)



# Starting camera thread
root.after(1, start_camera_thread)

root.mainloop()
# After closing window
camera.release()
