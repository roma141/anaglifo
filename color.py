import cv2
import numpy as np

def inc(val):
	if val<255:
		val += 1
	return val

def dec(val):
	if val>0:
		val -= 1
	return val


img = np.zeros([900, 900, 3], dtype=np.uint8)
img[:, :, :] = 255

rojo = 0
verde = 0
azul = 0


while True:
	derecho = (azul, verde, rojo)
	derecho = (255, 255, 141)
	izquierdo = (255, 0, 255)

	cv2.line(img, (10,10), (800,800), izquierdo, thickness=2)
	cv2.line(img, (10,30), (800,830), derecho, thickness=2)

	cv2.imshow('color', img)

	key = cv2.waitKey(1)
	print(derecho)
	# if key!=-1:
	# 	print(key) 
	if key == 27:
	    break
	elif key == 117: # u
	    rojo = inc(rojo)
	elif key == 106: # j
	    rojo = dec(rojo)
	elif key == 105: # i
	    verde = inc(verde)
	elif key == 107: # k
	    verde = dec(verde)
	elif key == 111: # o
	    azul = inc(azul)
	elif key == 108: # l
	    azul = dec(azul)

cv2.destroyAllWindows()

'''
(255, 255, 141) derecho
(255, 0, 255) izquierdo

'''