import cv2
import numpy as np


class Number:
    def __init__(self, number):
        DIRECTORY = "C:/Users/Alex/PycharmProjects/MinesweeperBot/dataset/"
        self.number = number
        self.path = DIRECTORY + str(self.number) + ".jpg"

    def compare(self, board_img):
        num_img = cv2.imread(self.path)
        gray = cv2.cvtColor(num_img, cv2.COLOR_BGR2GRAY)
        ret, num_img = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        return num_img.shape == board_img.shape and not (np.bitwise_xor(num_img, board_img).any())

    def getNumber(self):
        return self.number
