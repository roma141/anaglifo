import cv2
import numpy as np 

img = cv2.imread('chicabw.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
print(img.shape)
cv2.imshow('chica', img)
cv2.waitKey(0)
cv2.destroyAllWindows()