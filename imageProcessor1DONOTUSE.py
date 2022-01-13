# this file might be working or not
# imageProcessor3.py is simpler

# by m244zhu, 2021
# This file receives coordinates from one side of a cube (6 times)
# and returns the rgb values for each coordiante

# HOW IT IS DONE:
# gets a matrix of points from each coordinate
# gets rgb values of each matrix point
# takes the average rgb values per coordinate
# filters the rgb values by comparing average with raw values
# returns a list of 9 rgb values (one for each sqaure)

import cv2
import numpy as np

SIDE_COLOR_POINTS = 5
MATRIX = pow(SIDE_COLOR_POINTS, 2)
_OFF = 15
FILTER_DISPLACEMENT = 2
COLOR_NUMBER = 3 #rgb are only three colors
CUBE_SQUARES = 9

_X0 = 250
_X1 = 680
_X2 = 1130
_Y0 = 240
_Y1 = 690
_Y2 = 1115

# _X0 = 350
# _X1 = 1030
# _X2 = 1700
# _Y0 = 345
# _Y1 = 1025
# _Y2 = 1710
PIECE_NUM = 9
image = cv2.imread('faceB.jpeg')

coordinate0 = _X0, _Y0
coordinate1 = _X1, _Y0
coordinate2 = _X2, _Y0
coordinate3 = _X2, _Y1
coordinate4 = _X2, _Y2
coordinate5 = _X1, _Y2
coordinate6 = _X0, _Y2
coordinate7 = _X0, _Y1
coordinate8 = _X1, _Y1

coordinateList = [coordinate0, coordinate1, coordinate2, coordinate3, 
coordinate4, coordinate5, coordinate6, coordinate7, coordinate8]

# get a x, y coordinate and put it in a list = [x , y]
def coordToXY(coordinate):
    x, y = coordinate
    point = [x , y]
    return point

# from one coordinate, returns a list with nine coordinates
# from one dimensional cooridnate, create more coordinate around this coordinate
# this wil be used to create a matrix (that's the reason for repeated numbers)
# these numbers are the rows (y values) or columns (x values)
def oneDimensionalList(oneDcoord):
    oneDList = []
    newPoint = 0
    remainder = -1

    for i in range(SIDE_COLOR_POINTS):
        for j in range(SIDE_COLOR_POINTS):

            remainder = j%SIDE_COLOR_POINTS

            if remainder == 0: newPoint = oneDcoord - _OFF*2
            elif remainder == 1: newPoint = oneDcoord - _OFF
            elif remainder == 2: newPoint
            elif remainder == 3 : newPoint = oneDcoord + _OFF
            else: newPoint = oneDcoord = oneDcoord + _OFF*2
            
            oneDList.append(newPoint)

    return oneDList

# gets two list and combine them into one (same size)
# gets list x and list y and returns list x, y
def twoDimensionalList(xList, yList):
    xyList = []
    coordinate = 0, 0
    
    for i in range(pow(SIDE_COLOR_POINTS, 2)):
        coordinate = xList[i], yList[i]
        xyList.append(coordinate)
    
    return xyList

# get rgb color form matrix point
# return a list with rgb lists
def getRGB(coord, image):
    RGBList = []

    for i in range(MATRIX):
        [B, G, R] = image[coord[i]]
        RGBList.append([R, G, B])

    return RGBList

# find average for rgb values of the matrix point
# return a list [r, g, b]
def RGBAverage(RGBList):
    average = [-1 , -1, -1]
    invalid = -1    # used after the filter

    for i in range(COLOR_NUMBER):
        sum = 0
        totalColors = 0

        for j in range(MATRIX):
            color = RGBList[j][i]

            if color != invalid:
                sum += color
                totalColors += 1


        if totalColors > 0: average[i] = sum//totalColors
    
    return average;


# compares RGBList values with average, remove values that are too off from average
# returns the RGBList with failed colors [-1, -1, -1]
def filterRGB(RGBList, average):
    fail = [-1, -1, -1]

    for i in range(COLOR_NUMBER):
        min = average[i] - FILTER_DISPLACEMENT
        max = average[i] + FILTER_DISPLACEMENT

        for j in range(MATRIX):
            color = RGBList[j][i]

            if ((color < min) or (color > max)) and (color != -1):
                RGBList[j] = fail
    
    return RGBList




def main():
    
    imageLine = cv2.line(image, (0,0), (680,240), (255, 0, 0),1)
    imageLine = cv2.line(imageLine, (680,240), (680 - _OFF,240 - _OFF), (0, 255, 0),1)
    imageLine = cv2.line(imageLine, (680,240), (680,240 - _OFF), (0, 255, 0),1)
    imageLine = cv2.line(imageLine, (680,240), (680 + _OFF,240 - _OFF), (0, 255, 0),1)
    imageLine = cv2.line(imageLine, (680,240), (680 - _OFF,240), (0, 255, 0),1)
    imageLine = cv2.line(imageLine, (680,240), (680 + _OFF,240), (0, 255, 0),1)
    imageLine = cv2.line(imageLine, (680,240), (680 - _OFF,240 + _OFF), (0, 255, 0),1)
    imageLine = cv2.line(imageLine, (680,240), (680,240 + _OFF), (0, 255, 0),1)
    imageLine = cv2.line(imageLine, (680,240), (680 + _OFF,240 + _OFF), (0, 255, 0),1)

    cv2.imwrite("lineImage.png", imageLine)    
    print("done")

    for i in range(CUBE_SQUARES):

        pointList = coordToXY(coordinateList[i])

        xList = oneDimensionalList(pointList[0])
        yList = oneDimensionalList(pointList[1])

        mainList = twoDimensionalList(xList, yList)
        # print(f'Main list: {mainList}')

        RGBList = getRGB(mainList, image)
        # print(RGBList)

        average = RGBAverage(RGBList)
        # print(f"Average:{average}")

        filteredRGBList = filterRGB(RGBList, average)
        # print(f"Filtered RGB List:{filteredRGBList}")

        newAverage = RGBAverage(filteredRGBList)
        # print(f'New Average:{newAverage}')


        print(f'Index:{i} , coordinate:{coordinateList[i]}, average:{newAverage}')
        



if __name__ == '__main__': main()