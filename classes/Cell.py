class Cell:
    def __init__(self, coords, value):
        self.coords = coords
        self.value = value

    def getCoords(self):
        return self.coords

    def getValue(self):
        return self.value
