import tkinter as tk


def update_value(*args):
    value = args[0]
    obj = args[1]
    obj.config(text=f"Value of slider: {value}")


def setting_hide(setting_frame, main_frame):
    setting_frame.pack_forget()
    main_frame.pack(fill='both', expand=True)


def filters_setting(root, main_frame):
    # Hiding widgets
    main_frame.pack_forget()

    # Creating frame and exit button
    setting_frame = tk.Frame(root)
    exit_settings = tk.Button(setting_frame, text='Exit settings',
                              command=lambda: setting_hide(setting_frame, main_frame))
    exit_settings.pack()

    # Content of settings
    title = tk.Label(setting_frame, text='Filters Setting')

    slider_text = tk.Label(setting_frame, text="Value of slider: 0")
    slider = tk.Scale(setting_frame,
                      from_=0, to=100, orient="horizontal",
                      command=lambda value: update_value(value, slider_text)
                      )

    title.pack()
    slider.pack()
    slider_text.pack()
    setting_frame.pack()


def app_setting(root, main_frame):
    main_frame.pack_forget()

    # Creating frame and exit button
    setting_frame = tk.Frame(root)
    exit_settings = tk.Button(setting_frame, text='Exit settings',
                              command=lambda: setting_hide(setting_frame, main_frame))
    exit_settings.pack()

    # Content of settings
    title = tk.Label(setting_frame, text='Filters Setting')

    slider_text = tk.Label(setting_frame, text="Value of slider: 0")
    slider = tk.Scale(setting_frame,
                      from_=0, to=100, orient="horizontal",
                      command=lambda value: update_value(value, slider_text)
                      )

    title.pack()
    slider.pack()
    slider_text.pack()
    setting_frame.pack()
