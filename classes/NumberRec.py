import pytesseract


class NumberRec:
    def __init__(self, img):
        pytesseract.pytesseract.tesseract_cmd = 'D:/Program Files/Tesseract-OCR/tesseract.exe'
        self.number = pytesseract.image_to_string(img)

    def getNumber(self):
        return self.number
