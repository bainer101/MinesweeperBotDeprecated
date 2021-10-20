import cv2

from classes.Board import Board
from classes.ImgRec import ImgRec
from classes.NumberRec import NumberRec
from enums.Difficulty import Difficulty

board = Board()
imgRec = ImgRec(1, Difficulty.EXPERT, board)


def main():
    # TODO: THIS IS TEMPORARY, ASK USER TO WAIT UNTIL CORRECT BOARD DISPLAYED
    imgRec.getBoardDimensions()
    imgRec.getImg()

    imgRec.findContours()
    # cv2.drawContours(cropped, contours, -1, (0, 255, 0), 3)

    board.getCellDimensions(imgRec.getContours())
    board.createBoard()
    imgRec.genCells()
    print(board.getBoard()[0][0].getCoords())

    num_rec = NumberRec()

    while True:
        imgRec.updateImg()


        cv2.imshow('Board', imgRec.getImg())

        k = (cv2.waitKey(1) & 0xFF)
        if k == ord('q'):
            cv2.destroyAllWindows()
            break
        elif k == ord('s'):
            filename = input("What number is this? ") + ".jpg"
            cv2.imwrite("dataset/"+filename, imgRec.getCell())


if __name__ == '__main__':
    main()
