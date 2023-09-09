import json
import numpy as np
import cv2 as cv


class CameraClass:
    def __init__(self, window_number):
        """ Init function of CameraClass

        :param window_number: number of clicked tab
        """
        self.active_window_number = window_number
        # Default filter is default (0)
        self.active_filter = 0
        # Attribute that informs if settings are already displayed
        self.settings_displayed = 0

    @staticmethod
    def check_settings(*to_return):
        data_to_return = []

        # Opening setting file
        with open('settings/settings.json') as file:
            data = json.load(file)

        # Searching setting file for certain setting and adding it to array that will be returned
        for setting in to_return:
            data_to_return.append(data[setting])

        return data_to_return

    @staticmethod
    def update_settings(settings_value_dict):
        # Opening setting file
        with open('settings/settings.json', 'r') as file:
            data = json.load(file)

        # Updating data
        for key, value in settings_value_dict.items():
            # Calculating original ratio between numbers in setting array
            ratio = []
            for i in data[key]:
                if i:
                    ratio.append(i/data[key][0])
                else:
                    ratio.append(1)

            # Multiplying ratio elements by value
            value_array = [int(i*float(value)) for i in ratio]
            data[key] = value_array

        # Saving new data
        with open('settings/settings.json', 'w') as file:
            json.dump(data, file)

    # Filter functions
    @staticmethod
    def default(frame):
        frame = CameraClass.result_filters(frame)
        return np.uint8(frame)

    @staticmethod
    def gray(frame):
        frame = CameraClass.result_filters(frame)

        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        return cv.cvtColor(gray, cv.COLOR_GRAY2BGR)

    @staticmethod
    def laplacian(frame):
        frame = CameraClass.result_filters(frame)

        laplacian = cv.Laplacian(frame, cv.CV_64F)
        return np.uint8(laplacian)

    @staticmethod
    def blur(frame):
        frame = CameraClass.result_filters(frame)

        ksize = CameraClass.check_settings('blur_ksize')[0]
        blur = cv.blur(frame, ksize)
        return np.uint8(blur)


    @staticmethod
    def result_filters(frame):
        """Function to apply light filters (brighness etc.) before using main filter"""

        # Brighness
        brighness_setting = CameraClass.check_settings('brighness')[0][0]
        if brighness_setting:
            frame = CameraClass.brighness(frame)

        # Smooth effect
        bilateral_setting = CameraClass.check_settings('bilateral_filter')[0]
        if bilateral_setting:
            frame = CameraClass.bilateral(frame)

        return frame

    @staticmethod
    def bilateral(frame):
        setting = CameraClass.check_settings('bilateral_filter')[0]
        bilateral_frame = cv.bilateralFilter(frame, setting[0], setting[1], setting[2])
        return bilateral_frame

    @staticmethod
    def brighness(frame):
        setting = CameraClass.check_settings('brighness')[0][0]
        # Calculating alpha multiplayer
        setting = 1 + setting/100
        brighness_frame = cv.convertScaleAbs(frame, alpha=setting, beta=0)
        return brighness_frame

