# by m244zhu, Dec 2021
# this file is responsible to take pictures of the cube
# currently, cube needs to be manually changed to show different sides
# the goal is to have a robot to to this in the near future

from picamera import PiCamera
from time import sleep

CUBE_SIDES = 6
# can change these constants
PHOTO_TIME = 5              # time displaying the cube before taking a picture
INTERVAL = 10                # time between each displa
# directories where pictures are saved
DIRECTORY_FULL_COLOR = "/media/pi/SANDISK32GB/projectPenDrive/cubeFullColor/sideFullColor"
DIRECTORY = "/media/pi/SANDISK32GB/projectPenDrive/cubeSides/side"

camera = PiCamera()

# get index number and boolean "isFullColor" of a side 
# and take a picture of the side with photo number on it
# different value for isFullColor goes to different directories
# this is necessary for the program to "know" the colors of the cube (isFullColor = True)
def takeSidePicture(index, isFullColor):

    camera.start_preview()
    camera.exposure_mode = 'off'
    camera.annotate_text = f"Photo: {index}"
    sleep(PHOTO_TIME)
    
    if isFullColor:
        camera.capture(f'{DIRECTORY_FULL_COLOR}{index}.jpg')
    else:
        camera.capture(f'{DIRECTORY}{index}.jpg')

    camera.stop_preview()

# take six pictures, with an INTERVAL between each picture
def takeCubePicture(isFullColor):

    for side in range(CUBE_SIDES):
        takeSidePicture(side, isFullColor)
        sleep(INTERVAL)

# this function is intented to help calibrate the camera (position) and lights
def displayCameraView(time):
    camera.start_preview()
    sleep(time)
    camera.stop_preview()

def main():

    displayCameraView(30)

    # isFullColor = True
    # takeCubePicture(isFullColor)



if __name__ == '__main__': main()