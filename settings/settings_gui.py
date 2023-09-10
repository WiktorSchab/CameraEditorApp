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
        print(settings_to_update)
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


# Function to create slider with label with text
def slider_constructor(surrounding, setting_to_change, text, range_v):
    # Unpacking list with variables with info about surrounding of slider
    frame_tk = surrounding[0]
    instance = surrounding[1]
    setting_dict = surrounding[2]

    if len(range_v) == 3:
        value_jump = range_v[-1]
    else:
        value_jump = 1

    slider_value = instance.check_settings(setting_to_change)[0][0]

    blur_slider_text = tk.Label(frame_tk, text=f" {text}: {slider_value}")
    blur_slider = tk.Scale(frame_tk,
                           from_=range_v[0], to=range_v[1], orient="horizontal",
                           command=lambda value: update_value(value, blur_slider_text, setting_to_change, setting_dict),
                           resolution=value_jump
                           )
    # Setting value of slider by using function that check settings.json file
    blur_slider.set(slider_value)
    return blur_slider, blur_slider_text

# Function to save settings about virtual glasses
def bool_value_button(*args):
    obj = args[0]
    state = obj.cget('text')
    setting_name = args[1]
    settings_to_update = args[2]

    if state == 'OFF':
        obj.config(text='ON')
        settings_to_update[setting_name] = 1
    else:
        obj.config(text='OFF')
        settings_to_update[setting_name] = 0
    return


def filters_setting(root, main_frame, camera_instance):
    # Dictionary that contains what setting was changed and what value is new
    settings_to_update = {}

    # List elements to pack on window
    content_to_pack = []

    # Hiding widgets
    main_frame.pack_forget()

    # Creating frame and exit button
    setting_frame = tk.Frame(root)
    exit_settings = tk.Button(setting_frame, text='Exit settings',
                              command=lambda: exit_settings_funct(setting_frame, camera_instance, main_frame, settings_to_update))
    exit_settings.pack()

    # Content of settings
    title = tk.Label(setting_frame, text='Filters Setting')

    # List with info about where slider will be
    surroundings_for_slider = [setting_frame, camera_instance, settings_to_update]

    # Blur Settings
    content_to_pack.extend(
        slider_constructor(surroundings_for_slider, 'blur_ksize', 'blur strength', [1, 20]))

    # Bilateral Settings
    content_to_pack.extend(
        slider_constructor(surroundings_for_slider, 'bilateral_filter', 'bilateral strength', [1, 20]))

    # Brighness Settings
    content_to_pack.extend(
        slider_constructor(surroundings_for_slider, 'brighness', 'brighness strength', [-100, 100, 5]))

    # Yes/No button glasses
    glasses_text = tk.Label(setting_frame, text='Virtual glasses:')
    glasses_switch = tk.Button(setting_frame, text="OFF", command=lambda: bool_value_button(
        glasses_switch, 'glasses', settings_to_update))

    content_to_pack.extend([glasses_text,glasses_switch])

    if not camera_instance.settings_displayed:
        title.pack()

        # Displaying generated objects
        for obj in content_to_pack:
            obj.pack()

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
