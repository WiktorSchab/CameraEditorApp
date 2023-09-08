import tkinter as tk
from tkinter import messagebox

def update_value(*args):
    value = args[0]
    obj = args[1]
    setting_name = args[2]
    settings_to_update = args[3]

    # Getting proper format of text to add value
    text_obj = obj.cget('text')
    text_without_value = text_obj.split(':')[0]

    # Displaying text
    obj.config(text=f"{text_without_value}: {value}")

    settings_to_update[setting_name] = value


def exit_settings_funct(setting_frame, camera_instance, main_frame, settings_to_update):
    while 1:
        if settings_to_update:
            res = tk.messagebox.askquestion(title='Saving settings', message='Do you wanna to apply these settings?')
            if res == 'yes':
                # Sending data to update settings file
                camera_instance.update_settings(settings_to_update)

            # In the next loop iteration part code in else will be executed
            settings_to_update = {}

        else:
            # Hiding settings and showing main window
            setting_frame.pack_forget()

            # Changing attribute to 0, so settings will be displayed on next
            camera_instance.settings_displayed = 0
            main_frame.pack(fill='both', expand=True)
            return


def filters_setting(root, main_frame, camera_instance):
    # Dictionary that contains what setting was changed and what value is new
    settings_to_update = {}

    # Hiding widgets
    main_frame.pack_forget()

    # Creating frame and exit button
    setting_frame = tk.Frame(root)
    exit_settings = tk.Button(setting_frame, text='Exit settings',
                              command=lambda: exit_settings_funct(setting_frame, camera_instance, main_frame, settings_to_update))
    exit_settings.pack()

    # Content of settings
    title = tk.Label(setting_frame, text='Filters Setting')

    # Blur Settings
    blur_slider_text = tk.Label(setting_frame, text=" blur strength: 10")
    blur_slider = tk.Scale(setting_frame,
                      from_=1, to=20, orient="horizontal",
                      command=lambda value: update_value(value, blur_slider_text, 'blur_ksize', settings_to_update)
                      )
    # Setting value of slider by using function that check settings.json file
    blur_slider.set(camera_instance.check_settings('blur_ksize')[0][0])

    # Bilateral Settings
    bilateral_slider_text = tk.Label(setting_frame, text=" bilateral strength: 10")
    bilateral_slider = tk.Scale(setting_frame,
                      from_=1, to=20, orient="horizontal",
                      command=lambda value: update_value(value, bilateral_slider_text, 'bilateral_filter', settings_to_update)
                      )
    # Setting value of slider by using function that check settings.json file
    bilateral_slider.set(camera_instance.check_settings('bilateral_filter')[0][0])

    if not camera_instance.settings_displayed:
        title.pack()

        blur_slider.pack()
        blur_slider_text.pack()

        bilateral_slider.pack()
        bilateral_slider_text.pack()

        setting_frame.pack()

    # Changing setting displayed to 1 to avoid double objects on window
    camera_instance.settings_displayed = 1


def app_setting(root, main_frame, camera_instance):
    # Dictionary that contains what setting was changed and what value is new
    settings_to_update = {}

    main_frame.pack_forget()

    # Creating frame and exit button
    setting_frame = tk.Frame(root)
    exit_settings = tk.Button(setting_frame, text='Exit settings',
                              command=lambda: exit_settings_funct(setting_frame, camera_instance, main_frame, settings_to_update))
    exit_settings.pack()

    # Content of settings
    title = tk.Label(setting_frame, text='App Setting')

    if not camera_instance.settings_displayed:
        title.pack()
        setting_frame.pack()

        # Changing setting displayed to 1 to avoid double objects on window
        camera_instance.settings_displayed = 1
