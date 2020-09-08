import numpy as np
import cv2

def show(img):
    cv2.imshow("frame", img)
    while True:
        key = cv2.waitKey(1) 
        if key == 27:
            break

img = np.zeros((100, 200, 4), dtype = np.uint8)  # create image
# img[:,:,3] = 255                                 # set alpha to full
# img[30:70, 40:90, 0:3] = 255  # filled rectangle
img[30, 40:60, 0:3] = 255  # horizontal line
img[30:70, 40, 0:3] = 255  # vertical line
img[70, 40:60, 0:3] = 255  # horizontal line
img[30:70, 60, 0:3] = 255  # vertical line

show(img)