import cv2
import numpy as np 
import math
import time


def make_anag(img, x, y):
	(rows,cols, _) = img.shape
	imgl = np.zeros(img.shape, dtype=np.uint8)
	M = np.float32([[1,0,x], [0,1,y]])
	imgl[:, :, 1] = cv2.warpAffine(img[:, :, 1], M, (cols,rows)) # izquierda

	# El derecho es el magenta (red + blue) -> magenta
	imgr = np.zeros(img.shape, dtype=np.uint8)
	imgr[:, :, 2] = img[:, :, 2]		# R -> R
	# imgr[:, :, 1] = imgl				# G -> G
	imgr[:, :, 0] = img[:, :, 0]		# B -> B
	# print('magenta', img[:,:,2])
	return imgl, imgr

def rotate(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result


img = cv2.imread('2443toda.jpg')
img = cv2.pyrDown(img)
# img = rotate(img, 1.4)
imgl, imgr = make_anag(img, -100, 10)

uno = True
while True:
	if uno:
		cv2.imshow('val', imgr)
	else:
	# # time.sleep(.0001)
	# key = cv2.waitKey(1)
		cv2.imshow('val', imgl)	
	uno = not uno
	key = cv2.waitKey(2)
	if key == 27:
	    break


cv2.destroyAllWindows()