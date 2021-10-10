import cv2


class Board:
    def __init__(self):
        self.board = []
        self.x, self.y = 1, 1

    def getCellDimensions(self, c):
        x_start, y_start = 0, 0

        for contour in c:
            x, y, w, h = cv2.boundingRect(contour)

            if x_start == 0:
                x_start = x
                y_start = y
            elif x == x_start:
                self.x += 1
            elif y == y_start:
                self.y += 1

    def createBoard(self):
        for x in range(self.x):
            self.board.append([])
            for y in range(self.y):
                self.board[x].append(0)

    def viewBoard(self):
        for row in self.board:
            print(row)
