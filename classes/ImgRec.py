from mss import mss
import numpy as np
import ctypes
import cv2


class ImgRec:
    def __init__(self, mon_num, difficulty):
        self.mon_num = mon_num
        self.difficulty = difficulty

        self.user32 = ctypes.windll.user32
        self.mw, self.mh = self.user32.GetSystemMetrics(0), self.user32.GetSystemMetrics(1)

        self.sct = mss()
        self.mon = self.sct.monitors[self.mon_num]

        self.bounding_box = {
            'top': self.mon["top"],
            'left': self.mon["left"],
            'width': self.mw,
            'height': self.mh,
            "mon": self.mon_num
        }

        self.sct_img = None
        self.updateImg()

        self.contours = None
        self.findContours()
        self.dims = self.getBoardDimensions()

    def findContours(self):
        gray = cv2.cvtColor(self.sct_img, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 127, 255, 0)

        edges = cv2.Canny(thresh, 30, 200)
        c, hierarchy = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        self.contours = c

    def getBoardDimensions(self):
        sorted_contours = sorted(self.contours, key=cv2.contourArea, reverse=True)
        # 0 = Expert, 1 = Intermediate, 3 = Beginner
        # 200% Display, Light theme
        largest = sorted_contours[self.difficulty]

        x, y, w, h = cv2.boundingRect(largest)

        return x, y, w, h

    def crop2ROI(self):
        x, y, w, h = self.dims
        self.sct_img = self.sct_img[y:y + h, x:x + w]

    def updateImg(self):
        self.sct_img = np.array(self.sct.grab(self.bounding_box))

    def getContours(self):
        return self.contours

    def getImg(self):
        self.crop2ROI()
        return self.sct_img
