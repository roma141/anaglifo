import cv2
import numpy as np 

class Zoom(object):
	def __init__(self, window, img):
		self.window = window
		self.img0 = img
		self.img = img

		self.left_clicked = False
		self.xm0, self.ym0 = 0,0

		cv2.namedWindow(self.window)
		cv2.setMouseCallback(self.window, self.onmouse)

		self.img =  cv2.resize(img, (850, 1000), interpolation=cv2.INTER_LINEAR)
		self.nwindow = "zoom"
		self.show()

		
	def show(self):
		# print(self.img.shape)
		cv2.moveWindow(self.nwindow,400,0)
		while True:
			cv2.imshow(self.nwindow, self.img)
			key = cv2.waitKey(1)
			if key != -1:
				print(key) 
			
			if key == 27:
				break
		
		cv2.destroyAllWindows()

	def onmouse(self, event, x, y, flags, param):
		if event == cv2.EVENT_LBUTTONDOWN:
			self.left_clicked = True
			self.xm0, self.ym0 = x, y		

		elif event == cv2.EVENT_LBUTTONUP:
			if self.left_clicked:
				if self.xm0 > x:
					self.xm0, x = x, self.xm0
				if self.ym0 > y:
				 	self.ym0, y = y, self.ym0

				ancho, alto = (x - self.xm0), (y - self.ym0)
				propor = self.img.shape[0] / self.img.shape[1]
				k = alto / ancho
				if propor >= 1:
					if k < 1:
						alto = int(ancho * propor)
					else:
						ancho = int(alto / propor)

				self.img = self.img[self.ym0: self.ym0 + alto, self.xm0: self.xm0 + ancho]
				self.img =  cv2.resize(self.img, (850, 1000), interpolation=cv2.INTER_LINEAR)

				self.left_clicked = False

		elif event == cv2.EVENT_RBUTTONDOWN:
			self.img =  cv2.resize(self.img0, (850, 1000), interpolation=cv2.INTER_LINEAR)


img = cv2.imread('ValtodaD.jpg')
Zoom('zoom', img)





