# Separa anaglifo en las dos partes izquierda y derecha

import cv2
import numpy as np 

def show(window, img):
    print(img.shape)
    cv2.imshow(window, img)
    while True:
        key = cv2.waitKey(1)
        print(key) 
        if key == 27:
            break
    cv2.destroyAllWindows()

def sepanag(img):
	(rows, cols, _) = img.shape

	imgi = np.zeros([rows,cols, 3], dtype=np.uint8)
	imgi[:, :, 2] = img[:, :, 1]
	imgi[:, :, 1] = img[:, :, 1]
	imgi[:, :, 0] = img[:, :, 1]
	imgi = cv2.cvtColor(imgi, cv2.COLOR_BGR2GRAY)

	imgd = np.zeros([rows,cols, 3], dtype=np.uint8)
	imgd[:, :, 2] = img[:, :, 2]
	imgd[:, :, 1] = img[:, :, 2]
	imgd[:, :, 0] = img[:, :, 0]
	imgd = cv2.cvtColor(imgd, cv2.COLOR_BGR2GRAY)

	return imgi, imgd

img = cv2.imread('2443toda.jpg')
show('p3 img orig', img)

imgbw = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
show('p3 img bw', imgbw)

imgi, imgd = sepanag(img)

show('p3 imgi', imgi)
show('p3 imgd', imgd)


