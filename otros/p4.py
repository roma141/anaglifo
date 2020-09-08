# lista de todos los eventos que maneja open cv
import cv2 as cv
events = [i for i in dir(cv) if 'EVENT' in i]
print( events )
