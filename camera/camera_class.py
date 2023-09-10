import json
import re

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
                    ratio.append(i / data[key][0])
                else:
                    ratio.append(1)

            # Multiplying ratio elements by value
            value_array = [int(i * float(value)) for i in ratio]
            data[key] = value_array

        # Saving new data
        with open('settings/settings.json', 'w') as file:
            data = json.dumps(data, sort_keys=True)

            # Formatting text to have key and value in same lane
            data = re.sub(r',\s*"', ',\n"', data)
            data = '{\n' + data[1:-1] + '\n}'
            file.write(data)

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

        # Glasses on face
        glasses_setting = CameraClass.check_settings('glasses')[0][0]
        if glasses_setting:
            frame = CameraClass.glasses(frame)

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
        setting_br = CameraClass.check_settings('brighness')[0][0]
        # Calculating alpha multiplayer
        setting_br = 1 + setting_br / 100

        brighness_frame = cv.convertScaleAbs(frame, alpha=setting_br, beta=0)
        return brighness_frame

    @staticmethod
    def glasses(frame):
        glasses = cv.imread('glass_test.png', cv.IMREAD_UNCHANGED)

        face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')
        eye_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_eye.xml')

        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            eyes = eye_cascade.detectMultiScale(gray[y:y + h, x:x + w], 1.3, 5)

            if len(eyes) >= 2:
                # gh - glass height, ey - eyes y
                gh = h // 2

                ey = y + h // 2 - gh // 2
                # Placing glasses higher because they are by default placing below eyes
                ey = ey - gh // 4

                # Resizing glasses
                glasses_resized = cv.resize(glasses, (w, gh))

                # Extract the alpha channel from the glasses image
                alpha_channel = glasses_resized[:, :, 3] / 255.0

                # Calculate the complementary alpha channel
                frame_alpha = 1.0 - alpha_channel

                for c in range(0, 3):
                    frame[ey:ey + gh, x:x + w, c] = (alpha_channel * glasses_resized[:, :, c] +
                                                     frame_alpha * frame[ey:ey + gh, x:x + w, c])

        return frame
