import sys

from mss import mss
from .Cell import Cell

import numpy as np
import ctypes
import cv2


class ImgRec:
    def __init__(self, mon_num, difficulty, board):
        self.board = board
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
        self.last_frame = None
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

    def crop2ROI(self, dims):
        x, y, w, h = dims
        return self.sct_img[y:y + h, x:x + w]

    def isNewFrame(self):
        return not (self.sct_img.shape == self.last_frame.shape and not (
            np.bitwise_xor(self.sct_img, self.last_frame).any()))

    def updateImg(self):
        self.sct_img = np.array(self.sct.grab(self.bounding_box))

        if self.last_frame is None or self.isNewFrame():
            self.last_frame = self.sct_img

    def getContours(self):
        return self.contours

    def getDims(self):
        return self.dims

    def getImg(self):
        self.sct_img = self.crop2ROI(self.dims)
        return self.sct_img

    def genCells(self):
        seen_ys = []
        curr_y = -1
        for c in self.contours:
            x, y, w, h = cv2.boundingRect(c)
            curr_coords = []

            if y not in seen_ys and w / self.dims[2] < 0.5 and h / self.dims[3] < 0.5:
                curr_y += 1
                seen_ys.append(y)
                for c2 in self.contours:
                    x2, y2, w2, h2 = cv2.boundingRect(c2)
                    if y == y2 and x != x2 and 0 < y2 and 0 < x2 and w2 / self.dims[2] < 0.5 and h2 / self.dims[3] < 0.5:
                        curr_coords.append((x2, y2))

                sorted_curr_coords = sorted(curr_coords, key=lambda tup: tup[0])
                print(len(sorted_curr_coords))
                for i, coord in enumerate(sorted_curr_coords):
                    self.board.addCell((curr_y, i), Cell(coord, None))


