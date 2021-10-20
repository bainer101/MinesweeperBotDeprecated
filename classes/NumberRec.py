from .Number import Number
import cv2


class NumberRec:
    def __init__(self):
        self.numbers = [Number(x) for x in range(1, 9)]

    def check(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, img = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        for num in self.numbers:
            if num.compare(img):
                return num.number

        return None
