# by m244zhu, Jan 2022
# this file take pictures of the cube (solved and unsolved)
# and returns a color index array for the solving algorithm (writting on Rubik's Cube Part II)

import imageGetter
import imageProcessor3
import color

# these values might need to be changed
rawPoints = [630, 915, 1200, 260, 540, 820]
DIRECTORY_FULL_COLOR = "/media/pi/SANDISK32GB/projectPenDrive/cubeFullColor/sideFullColor"
DIRECTORY = "/media/pi/SANDISK32GB/projectPenDrive/cubeSides/side"
BOUNDARY = 60
WHITE_BOUNDARY = 30

def main():
    print('This is the main program')

    print('Do you need to take picture of cube in full color?')
    answer = input('yes/no: ')
    
    if answer == 'yes': 
        imageGetter.takeCubePicture(True)

    ready = ''

    while ready != 'ready' :     
        ready = input("Type 'ready' when you are ready to take pictures of the scrambled cube: ")

    imageGetter.takeCubePicture(False)

    rgbListFullColor = imageProcessor3.imageProcessorCube(rawPoints, DIRECTORY_FULL_COLOR)
    rgblistCube = imageProcessor3.imageProcessorCube(rawPoints, DIRECTORY)

    boundaryList = color.getBoundaryList(rgbListFullColor, BOUNDARY, WHITE_BOUNDARY)

    indexListFullColor = color.getColor(rgbListFullColor,boundaryList)

    indexListCube = color.getColor(rgblistCube, boundaryList)

    arrayList = [rgbListFullColor, rgblistCube, boundaryList, indexListFullColor, indexListCube]
    arrayName = ['rgbListFullColor:\n', '\nrgbListCube:\n', '\nboundaryList:\n', '\nindexListFullColor:\n', '\nindexListCube:\n']

    file = open('cubeMain.txt', 'w')
    for i in range(5):
        array = arrayList[i]
        file.write(f'{arrayName[i]}')
        for side in range(color.CUBE_SIDES):
            file.write(f'{array[side]}\n')
    

if __name__ == '__main__': main()