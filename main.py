import cv2

from classes.Board import Board
from classes.ImgRec import ImgRec
from classes.NumberRec import NumberRec
from enums.Difficulty import Difficulty

board = Board()
imgRec = ImgRec(1, Difficulty.EXPERT)


def main():
    # TODO: THIS IS TEMPORARY, ASK USER TO WAIT UNTIL CORRECT BOARD DISPLAYED
    imgRec.getBoardDimensions()
    imgRec.getImg()

    imgRec.findContours()
    # cv2.drawContours(cropped, contours, -1, (0, 255, 0), 3)

    board.getCellDimensions(imgRec.getContours())
    board.createBoard()
    board.viewBoard()

    while True:
        imgRec.updateImg()

        numberRec = NumberRec(imgRec.getCell())
        print(numberRec.getNumber())

        cv2.imshow('Board', imgRec.getImg())

        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()
