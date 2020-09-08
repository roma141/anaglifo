import numpy as np
import cv2

def show(img):
	# cv2.imshow("frame", img)
	i = 0
	while True:
		# img[30:70, 40:90, 1] = i
		# print(i)	
		cv2.imshow("frame", img)
		# i += 5
		# if i>255:
		# 	i = 0
		key = cv2.waitKey(10) 
		if key == 27:
			break

img = np.zeros((100, 200, 4), dtype = np.uint8)  # create image
# img[:,:,3] = 255                                 # set alpha to full
img[30:70, 40:90, 0:3] = 255  # filled rectangle

# img[30, 40:60, 0:3] = 255  # horizontal line
# img[30:70, 40, 0:3] = 255  # vertical line
# img[70, 40:60, 0:3] = 255  # horizontal line
# img[30:70, 60, 0:3] = 255  # vertical line

#color
img[30:70, 40:90, 2] = 255
img[30:70, 40:90, 1] = 169
img[30:70, 40:90, 0] = 49

# for i in range(0, 255, 10):
# 	img[30:70, 40:90, 1] = i
# 	print(i)
show(img)