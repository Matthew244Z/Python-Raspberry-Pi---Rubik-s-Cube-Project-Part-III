# Python-Raspberry-Pi---Rubik-s-Cube-Project-Part-III

Hello, this is the third part of the Rubik's Cube Project. On this part I focused on the computer vision of the project.

I was able to identify colors on a cube and return an array with the data for the solving algorithm (Parts I and II).

This was done using a **Raspberry Pi 4** and a **camera**. The **PiCamera** and **OpenCV** python libraries were used.

## Brief Overview

1 - Camera takes pictures of all sides full color (cube is not mixed).
*Cube needs to be moved manually at the moment. Plans for the future is to have a mechanical arm to do this.*
    
2 - Pictures are stored in a folder.

3 - Get rgb color of each piece (color) of all sides using **OpenCV** (9 pieces per side, 6 sides total).

4 - Get mean rgb color value for each color and add boundaries to the value.
*We now have a boundary for all colors*
    
5 - Mix cube and take picture again.

6 - Use boundary to identify colors.

7 - Return an array(6, 9) for the solving algorithm.
