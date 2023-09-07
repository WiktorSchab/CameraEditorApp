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

    # Filter functions
    @staticmethod
    def gray(frame):
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        return cv.cvtColor(gray, cv.COLOR_GRAY2BGR)

    @staticmethod
    def laplacian(frame):
        laplacian = cv.Laplacian(frame, cv.CV_64F)
        return np.uint8(laplacian)

    @staticmethod
    def blur(frame):
        ksize = CameraClass.check_settings('blur_ksize')[0]
        blur = cv.blur(frame, ksize)
        return np.uint8(blur)

    @staticmethod
    def bilateral(frame):
        setting = CameraClass.check_settings('bilateral_filter')[0]
        Bilateral = cv.bilateralFilter(frame, setting[0], setting[1], setting[2])
        return np.uint8(Bilateral)
