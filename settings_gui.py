import tkinter as tk


def update_value(*args):
    value = args[0]
    obj = args[1]
    obj.config(text=f"Value of slider: {value}")


def setting_hide(setting_frame, camera_instance, main_frame):
    setting_frame.pack_forget()

    # Changing attribute to 0, so settings will be displayed on next
    camera_instance.settings_displayed = 0
    main_frame.pack(fill='both', expand=True)


def filters_setting(root, main_frame, camera_instance):
    # Hiding widgets
    main_frame.pack_forget()

    # Creating frame and exit button
    setting_frame = tk.Frame(root)
    exit_settings = tk.Button(setting_frame, text='Exit settings',
                              command=lambda: setting_hide(setting_frame, camera_instance, main_frame))
    exit_settings.pack()

    # Content of settings
    title = tk.Label(setting_frame, text='Filters Setting')

    slider_text = tk.Label(setting_frame, text="Value of slider: 0")
    slider = tk.Scale(setting_frame,
                      from_=0, to=100, orient="horizontal",
                      command=lambda value: update_value(value, slider_text)
                      )

    if not camera_instance.settings_displayed:
        title.pack()
        slider.pack()
        slider_text.pack()
        setting_frame.pack()

    # Changing setting displayed to 1 to avoid double objects on window
    camera_instance.settings_displayed = 1


def app_setting(root, main_frame, camera_instance):
    main_frame.pack_forget()

    # Creating frame and exit button
    setting_frame = tk.Frame(root)
    exit_settings = tk.Button(setting_frame, text='Exit settings',
                              command=lambda: setting_hide(setting_frame, camera_instance, main_frame))
    exit_settings.pack()

    # Content of settings
    title = tk.Label(setting_frame, text='App Setting')

    slider_text = tk.Label(setting_frame, text="Value of slider: 0")
    slider = tk.Scale(setting_frame,
                      from_=0, to=100, orient="horizontal",
                      command=lambda value: update_value(value, slider_text)
                      )

    if not camera_instance.settings_displayed:
        title.pack()
        slider.pack()
        slider_text.pack()
        setting_frame.pack()

        # Changing setting displayed to 1 to avoid double objects on window
        camera_instance.settings_displayed = 1
