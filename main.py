import cv2

from classes.Board import Board
from classes.ImgRec import ImgRec
from enums.Difficulty import Difficulty

board = Board()
imgRec = ImgRec(1, Difficulty.BEGINNER)


def main():
    # TODO: THIS IS TEMPORARY, ASK USER TO WAIT UNTIL CORRECT BOARD DISPLAYED
    imgRec.getBoardDimensions()
    imgRec.crop2ROI()

    imgRec.findContours()
    # cv2.drawContours(cropped, contours, -1, (0, 255, 0), 3)

    board.getCellDimensions(imgRec.getContours())
    board.createBoard()
    board.viewBoard()

    while True:
        imgRec.updateImg()
        imgRec.crop2ROI()

        cv2.imshow('Board', imgRec.sct_img)

        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()
