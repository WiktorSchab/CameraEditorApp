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
        ksize = (10, 10)
        blur = cv.blur(frame, ksize)
        return np.uint8(blur)

    @staticmethod
    def bilateral(frame):
        Bilateral = cv.bilateralFilter(frame, 9, 75, 75)
        return np.uint8(Bilateral)
