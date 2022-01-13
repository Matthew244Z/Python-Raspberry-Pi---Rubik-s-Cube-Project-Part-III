# by m244zhu, Dec 2021
# this file receives an array of rgb values of all pieces and return an array with the indexes for the colors
# this array would be then used on the solving algorithm on Rubik's Cube Part II

import numpy as np
import imageProcessor3

COLOR_NUMBER = 3    # rgb are only three colors
CUBE_PIECES = 9     # number of pieces on one side
BOUNDARY = 45
WHITE_BOUNDARY = 30
CUBE_SIDES = 6      # total sides on a cube
# color indexes
YELLOW = 0
BLUE = 1
RED = 2
GREEN = 3
ORANGE = 4
WHITE = 5

rawPoints = [630, 915, 1200, 260, 540, 820]
DIRECTORY_FULL_COLOR = "/media/pi/SANDISK32GB/projectPenDrive/cubeFullColor/sideFullColor"
DIRECTORY = "/media/pi/SANDISK32GB/projectPenDrive/cubeSides/side"

# list = [
#     [[113, 139, 22], [116, 136, 9], [115, 135, 22], [122, 142, 20], [130, 157, 56], [131, 159, 60], [119, 152, 66], [122, 146, 21], [125, 146, 18]], 
#     [[0, 42, 125], [0, 36, 118], [4, 42, 117], [4, 47, 125], [16, 70, 143], [14, 73, 149], [14, 76, 150], [1, 43, 128], [0, 42, 127]], 
#     [[103, 31, 39], [106, 24, 32], [102, 30, 37], [109, 32, 43], [117, 55, 73], [116, 58, 79], [100, 66, 87], [99, 32, 42], [112, 26, 38]], 
#     [[0, 93, 74], [0, 87, 65], [0, 89, 71], [0, 92, 73], [1, 111, 101], [0, 114, 105], [6, 110, 105], [1, 94, 76], [0, 95, 74]], 
#     [[141, 83, 34], [140, 76, 29], [137, 79, 36], [146, 84, 40], [154, 104, 73], [155, 105, 78], [144, 105, 80], [143, 85, 37], [151, 85, 37]], 
#     [[121, 151, 159], [127, 153, 160], [126, 151, 156], [132, 156, 162], [144, 178, 186], [146, 181, 190], [136, 173, 183], [121, 148, 155], [138, 163, 171]]]

listFullColor = imageProcessor3.imageProcessorCube(rawPoints, DIRECTORY_FULL_COLOR)
list = imageProcessor3.imageProcessorCube(rawPoints, DIRECTORY)


# get rgbList of one side and return a list of separate rgb values. This helps calculate the mean values.
# input: list of rgb values for every piece on one side (size 9, 3)
# output: list of all red, green and blue values on one side (size 3, 9)
def separateRGB(rgbList):
    separateList = []
    
    for i in range(COLOR_NUMBER):
        color = []

        for j in range(CUBE_PIECES):
            color.append(rgbList[j][i])

        separateList.append(color)

    return separateList

# get a list of separate rgb values and return the mean of each color
# input: list of all red, green and blue values on one side (size 3, 9)
# output: list of the mean values for red, green and blue (size 3)
def getRGBValue(separateList):

    meanRGB = []

    for i in range(COLOR_NUMBER):
        value = np.mean(separateList[i])
        value = np.round_(value)
        # value = int(value)
        meanRGB.append(value)

    return meanRGB

# get a list of mean rgv values and boundary value and return the lower and upper boundaries for an rgb value
# input: list of the mean values for red, green and blue (size 3) and boundary number
# output: list of lower and upper boundary (size 2)
def getBoundary(meanRGB, boundary, side, whiteBoundary):

    TWO_BOUNDARIES = 2
    rgbBoundary = []
    rgbBoudnaryList = []
    value = 0

    for i in range(TWO_BOUNDARIES):

        for j in range(COLOR_NUMBER):

            if i == 0:                      # lower boundary
                value = meanRGB[j] - boundary
                # the white color seems to be hard to identify
                if side == WHITE: value = value - whiteBoundary
                if value < 0: value = 0     # the lowest value possible is 0
            else:                           # upper boundary
                value = meanRGB[j] + boundary
                if side == WHITE: value = value + whiteBoundary
                if value > 255: value = 255 # the highest value possible is 255

            rgbBoundary.append(value)
        rgbBoudnaryList.append(rgbBoundary)
        rgbBoundary = []        # reset list

    return rgbBoudnaryList


# get rgbList of one side and return the boundaries for the side color.
# note: this function should be called before the cube is scrambled.
#       the computer will use the boundaries found here to identify the colors on a scrambled cube.
# input: list of all rgb values on the cube (size 6, 9, 3) and boundary range
# output: list of all rgb boundaries (size 6, 2, 3)
def getBoundaryList(rgbList, boundaryRange, whiteBoundary):

    boundaryList = []

    for side in range (CUBE_SIDES):

        separateList = separateRGB(rgbList[side])
        rgbValue = getRGBValue(separateList)
        boundary = getBoundary(rgbValue, boundaryRange, side, whiteBoundary)
        boundaryList.append(boundary)

    return boundaryList


# this function should be called everytime the cube is being solved.
def getColor(rgbList, boundaryList):

    LOWER = 0
    UPPER = 1
    rgbRED = 0
    rgbGREEN = 1
    rgbBLUE = 2
    color = 0

    sideColor = []
    cubeColor = []

    colorFound = False

    for side in range (CUBE_SIDES):

        for piece in range (CUBE_PIECES):

            pieceRed = rgbList[side][piece][rgbRED]
            pieceGreen = rgbList[side][piece][rgbGREEN]
            pieceBlue = rgbList[side][piece][rgbBLUE]

            while(colorFound == False):
                
                lowerRed = boundaryList[color][LOWER][rgbRED]
                lowerGreen = boundaryList[color][LOWER][rgbGREEN]
                lowerBlue = boundaryList[color][LOWER][rgbBLUE]

                upperRed = boundaryList[color][UPPER][rgbRED]
                upperGreen = boundaryList[color][UPPER][rgbGREEN]
                upperBlue = boundaryList[color][UPPER][rgbBLUE]

                if (lowerRed <= pieceRed and lowerGreen <= pieceGreen and lowerBlue <= pieceBlue and
                    pieceRed <= upperRed and pieceGreen <= upperGreen and pieceBlue <= upperBlue):
                    sideColor.append(color)
                    colorFound = True
                else:
                    color = color + 1
                    if color == 6:
                        sideColor.append(-1)
                        colorFound = True

            colorFound = False
            color = 0

        cubeColor.append(sideColor)
        sideColor = []

    return cubeColor



def main():
    print('Start')
    
    boundaryList = getBoundaryList(listFullColor, BOUNDARY, WHITE_BOUNDARY)

    colorlist = getColor(listFullColor, boundaryList)

    colorlist2 = getColor(list, boundaryList)

    file = open('cube.txt', 'w')
    
    arrayList = [listFullColor, list, boundaryList, colorlist, colorlist2]
    arrayName = ['Full Color List:\n', '\nRGB List:\n', '\nBoundary List:\n', '\nColor List:\n', '\nColor List 2:\n']

    for i in range (5):
        array = arrayList[i]
        file.write(f'{arrayName[i]}')
        for side in range(CUBE_SIDES):
            file.write(f'{array[side]}\n')

    file.close()
    print('Done')


if __name__ == '__main__': main()