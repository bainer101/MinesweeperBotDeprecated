import numpy as np
import ctypes
import cv2
from classes.Board import Board

from mss import mss

board = Board()

sct = mss()
user32 = ctypes.windll.user32
mw, mh = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

mon_num = 1
mon = sct.monitors[mon_num]

bounding_box = {
    'top': mon["top"],
    'left': mon["left"],
    'width': mw,
    'height': mh,
    "mon": mon_num
}


def get_contour_areas(c):
    all_areas = []

    for cnt in c:
        area = cv2.contourArea(cnt)
        all_areas.append(area)
    return all_areas


def findContours(sct_img):
    gray = cv2.cvtColor(sct_img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 127, 255, 0)

    edges = cv2.Canny(thresh, 30, 200)
    c, hierarchy = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    return c


def getBoardDimensions(c):
    sorted_contours = sorted(c, key=cv2.contourArea, reverse=True)
    # 0 = Expert, 1 = Intermediate, 3 = Beginner
    # 200% Display, Light theme
    largest = sorted_contours[0]

    x, y, w, h = cv2.boundingRect(largest)

    return x, y, w, h


def crop2ROI(img, x, y, w, h):
    return img[y:y + h, x:x + w]


def main():
    window = np.array(sct.grab(bounding_box))
    dims = getBoardDimensions(findContours(window))
    cropped = crop2ROI(window, *dims)

    contours = findContours(cropped)
    # cv2.drawContours(cropped, contours, -1, (0, 255, 0), 3)

    board.getCellDimensions(contours)
    board.createBoard()
    board.viewBoard()

    while True:
        window = np.array(sct.grab(bounding_box))
        cropped = crop2ROI(window, *dims)

        cv2.imshow('Board', cropped)

        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()
