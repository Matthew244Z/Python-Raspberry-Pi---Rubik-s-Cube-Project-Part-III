# by m244zhu, Dec 2021
# this file receives pictures of the cube and returns an array of rgb values for all pieces

import cv2
import numpy as np

# constant values
_OFF = 50           # for ROI 
COLOR_NUMBER = 3    # rgb are only three colors
CUBE_PIECES = 9     # number of pieces on one side
CUBE_SIDES = 6      # total sides on a cube

# these values can be changed if necessary
rawPoints = [630, 915, 1200, 260, 540, 820]
DIRECTORY_FULL_COLOR = "/media/pi/SANDISK32GB/projectPenDrive/cubeFullColor/sideFullColor"
DIRECTORY = "/media/pi/SANDISK32GB/projectPenDrive/cubeSides/side"


# get a list with x and y coordinates, 3 of each
# return a list with 9 coordinate from the matrix
def getCoordinate(coordArray):
    X0 = coordArray[0]
    X1 = coordArray[1]
    X2 = coordArray[2]
    Y0 = coordArray[3]
    Y1 = coordArray[4]
    Y2 = coordArray[5]

    coordinate0 = X0, Y0
    coordinate1 = X1, Y0
    coordinate2 = X2, Y0
    coordinate3 = X2, Y1
    coordinate4 = X2, Y2
    coordinate5 = X1, Y2
    coordinate6 = X0, Y2
    coordinate7 = X0, Y1
    coordinate8 = X1, Y1

    coordinateList = [coordinate0, coordinate1, coordinate2, coordinate3, coordinate4, coordinate5, coordinate6, coordinate7, coordinate8]

    return coordinateList


# get x, y coordinates and return a list [x , y]
def coordToXY(coordinate):
    x, y = coordinate
    point = [x , y]
    return point


# get one point and return a list of two points
# these two points will define the area (square) for the color
# these two points are _OFF some distance from initial point
def twoPoints(oneDcoord):
    oneDList = [oneDcoord - _OFF, oneDcoord + _OFF]
    return oneDList


# get x and y points and return a region of interest
# this will be the area to identify the color
def getROI(xPoints, yPoints, image):
    # image[height, width] on openCV uses heigth and width
    return image[ yPoints[0] : yPoints[1], xPoints[0] : xPoints[1] ]


# get ROI image and return rgb colors in a list
# use opencv indexes to find b g r colors on image
# then calculate the mean using numpy
def getRGB(imageROI):
    # I supposed the first and second arguments are for the height and width of the image
    # and the third one is the color
    b = imageROI[:, :, 0]
    g = imageROI[:, :, 1]
    r = imageROI[:, :, 2]

    bMean = np.mean(b)
    gMean = np.mean(g)
    rMean = np.mean(r)

    rgbList = [int(rMean), int(gMean), int(bMean)]

    return rgbList


# get coordinate (x ,y), image and index
# return the rgb color of the coordinate
# this is the core function
def imageProcessor(coordinate, image):

    pointList = coordToXY(coordinate)

    xTwoPoints = twoPoints(pointList[0])
    yTwoPoints = twoPoints(pointList[1])

    roiImage = getROI(xTwoPoints, yTwoPoints, image)

    rgbList = getRGB(roiImage)

    return rgbList


# get rawPoints (three x and three y values) and directory for the images 
# and return a list of rgb values of all pieces on all sides
# the rawPoints are converted to a list of matrix coordinate for all pieces
def imageProcessorCube(rawPoints, directory):
    sideRGB = []
    cubeRGB = []

    coordinateList = getCoordinate(rawPoints)   # get matrix coordinate (list) of all 9 pieces

    for side in range(CUBE_SIDES):          # access all 6 sides of a cube

        image= cv2.imread(f'{directory}{side}.jpg')

        for index in range(CUBE_PIECES):    # access all 9 pieces of side
            
            rgbList = imageProcessor(coordinateList[index], image)
            sideRGB.append(rgbList)

        cubeRGB.append(sideRGB)
        sideRGB = []                # reset list

    return cubeRGB


# the next two functions are only used to check the pictures and region of interests (ROI)
# they do not affect the functionality of the program

# get name for a window and image
# display a window for the image
def display(name, image):
    cv2.imshow(name, image)
    cv2.waitKey()
    cv2.destroyAllWindows()


# save region of interest if it needs to be check 
def roiImage(coordinate, image, index):
    pointList = coordToXY(coordinate)

    xTwoPoints = twoPoints(pointList[0])
    yTwoPoints = twoPoints(pointList[1])

    roiImage = getROI(xTwoPoints, yTwoPoints, image)
    cv2.imwrite(f'/media/pi/SANDISK32GB/projectPenDrive/roiImages/roiImage{index}.jpeg', roiImage)


def main():
    
    print('Start')

    cubeRGBFullColor = imageProcessorCube(rawPoints, DIRECTORY_FULL_COLOR)
    cubeRGB = imageProcessorCube(rawPoints, DIRECTORY)

    print('Cube RGB FUll Color')
    print(cubeRGBFullColor)

    print('\nCube RGB')
    print(cubeRGB)
    print('\nProgram is done')


if __name__ == '__main__': main()