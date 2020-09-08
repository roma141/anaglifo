import numpy as np
import conversion
import cv2

def read_dic(filename):
    with open(filename, 'r') as f:
        dic = eval(f.read())    
    return dic

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

def make_anag(imgi, imgd, x, y):
    (rows,cols) = imgi.shape
    M = np.float32([[1,0,x], [0,1,y]])
    img0 = cv2.warpAffine(imgi, M, (cols,rows)) # izquierda

    # El derecho es el magenta (red + blue) -> magenta
    anag = np.zeros([rows,cols, 3], dtype=np.uint8)
    anag[:, :, 2] = imgd[:, :]        # R -> R
    anag[:, :, 1] = img0[:, :]                # G -> G
    anag[:, :, 0] = imgd[:, :]        # B -> B
    return anag

def make_anag1(img, x, y):
    (rows,cols, _) = img.shape
    M = np.float32([[1,0,x], [0,1,y]])
    img0 = cv2.warpAffine(img[:, :, 1], M, (cols,rows)) # izquierda

    # El derecho es el magenta (red + blue) -> magenta
    anag = np.zeros(img.shape, dtype=np.uint8)
    anag[:, :, 2] = img[:, :, 2]        # R -> R
    anag[:, :, 1] = img0                # G -> G
    anag[:, :, 0] = img[:, :, 0]        # B -> B
    return anag

def fit(img, anchoimg, altoimg, x, y):
    img = cv2.resize(img, (anchoimg, altoimg), interpolation=cv2.INTER_LINEAR)
    return make_anag(img, x, y)

def insert(grande, peq, x, y):
    if peq.shape[0] + x <= grande.shape[0] and peq.shape[1] + y <= grande.shape[1]:
        grande[y: y + peq.shape[0], x: x + peq.shape[1]] = peq
    return grande 


class Image(object):
    def __init__(self, contours, imgi, imgd):
        self.contours = contours
        self.dibcurvas = True
        self.dibimagen = True
        self.direccion = 'x'
        self.modoed = 'dib'

        self.anchoimg = 1000
        self.altoimg = 1000 # 1100 para el zanjon

        self.xsize = 700
        self.ysize = 697 # 620
        self.xpos = 300
        self.ypos = 221 #250


        self.parte = ''  # '', 'd', 'i'


        # self.p0 = 50
        self.poscurx = 7
        self.poscury = 0
        self.xanag = -125  # -220
        self.yanag = 42
        self.imgi = imgi
        self.imgd = imgd
        self.anag0 = make_anag(imgi, imgd, self.xanag, self.yanag)

        self.left_clicked = False
        self.right_clicked = False
        self.ctrl_clicked = False
        self.shift_clicked = False
        self.xm0, self.ym0 = 0,0

        cv2.namedWindow(contours.filename)
        cv2.setMouseCallback(contours.filename, self.onmouse)

        self.draw()
        self.show()


    def cabe(self):
        return  self.xsize + self.xpos <= self.anchoimg and self.ysize + self.ypos <= self.altoimg

    def dibujaImagen(self):
        self.imgr = np.zeros([self.anchoimg, self.altoimg, 3], dtype=np.uint8)
        self.imgl = np.zeros([self.anchoimg, self.altoimg, 3], dtype=np.uint8)
        self.img  = np.zeros([self.anchoimg, self.altoimg, 3], dtype=np.uint8)
        # self.img[:, :, :] = 255 # fondo blanco

        if self.dibimagen:
            imgx =  cv2.resize(self.anag0, (self.xsize, self.ysize), interpolation=cv2.INTER_LINEAR) # tamaño
            if self.cabe():
                self.anag = insert(self.img, imgx, self.xpos, self.ypos) # posicion
            
            if self.parte == '':
                self.imgl[:, :, 2] = self.anag[:, :, 2]        # R -> R
                self.imgl[:, :, 0] = self.anag[:, :, 0]        # B -> B
                self.imgr[:, :, 1] = self.anag[:, :, 1]        # G -> G

            elif self.parte == 'd':
                self.imgl[:, :, 2] = self.anag[:, :, 2]        # R -> R
                self.imgl[:, :, 0] = self.anag[:, :, 0]        # B -> B
                self.imgr[:, :, 1] = self.anag[:, :, 0]        # G -> G

            elif self.parte == 'i':
                self.imgl[:, :, 2] = self.anag[:, :, 1]        # R -> R
                self.imgl[:, :, 0] = self.anag[:, :, 1]        # B -> B
                self.imgr[:, :, 1] = self.anag[:, :, 1]        # G -> G

        else:
            self.imgr[:, :, :] = 255
            self.imgl[:, :, :] = 255

    def draw(self):
        self.dibujaImagen()     

        if self.dibcurvas:
            self.imgl, self.imgr = self.contours.draw(self.imgl, self.imgr, self.parte)

        self.img[:, :, 0] = self.imgl[:, :, 0]
        self.img[:, :, 1] = self.imgr[:, :, 1]
        self.img[:, :, 2] = self.imgl[:, :, 2]

    def onmouse(self, event, x, y, flags, param):

        if flags == cv2.EVENT_FLAG_CTRLKEY + cv2.EVENT_FLAG_LBUTTON:
            self.ctrl_clicked = True

        if flags == cv2.EVENT_FLAG_SHIFTKEY + cv2.EVENT_FLAG_LBUTTON:
            self.shift_clicked = True

        if event == cv2.EVENT_LBUTTONDOWN:
            self.left_clicked = True
            self.xm0, self.ym0 = x, y

        elif event == cv2.EVENT_RBUTTONDOWN:
            self.right_clicked = True
            self.xm0, self.ym0 = x, y

            if flags == cv2.EVENT_FLAG_CTRLKEY + cv2.EVENT_FLAG_LBUTTON:
                self.right_clicked = False
                self.ctrl_clicked = True
        
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.left_clicked and not self.ctrl_clicked and not self.shift_clicked and self.modoed=='ajuste': # ESCALA
                if self.direccion == 'y':
                    print('resize y', self.ysize)
                    delta = y - self.ym0
                    self.ym0 = y
                    ant = self.ysize
                    if delta>0:
                        self.ysize += 1
                    else:
                        self.ysize -= 1
                    
                    if self.cabe():
                        self.draw()
                    else:
                        self.ysize = ant 
                
                elif self.direccion == 'x':
                    print('resize x', self.xsize)
                    delta = x - self.xm0
                    self.xm0 = x
                    ant = self.xsize
                    if delta>0:
                        self.xsize += 1
                    else:
                        self.xsize -= 1
                    
                    if self.cabe():
                        self.draw()
                    else:
                        self.xsize = ant 

            if self.left_clicked and self.ctrl_clicked and not self.shift_clicked and self.modoed=='ajuste': # POSICION
                if self.direccion == 'y': # ??? cambiar a y
                    print('mueve y', self.ypos)
                    delta = y - self.ym0
                    self.ym0 = y
                    ant = self.ypos
                    if delta>0:
                        self.ypos += 1
                    else:
                        self.ypos -= 1
                    
                    if self.cabe():
                        self.draw()
                    else:
                        self.ypos = ant 
                
                elif self.direccion == 'x':
                    print('mueve x', self.xpos)
                    delta = x - self.xm0
                    print(delta, x, self.xm0)
                    self.xm0 = x
                    ant = self.xpos
                    if delta>0:
                        print('inc')
                        self.xpos += 1
                    else:
                        print('dec')
                        self.xpos -= 1
                    
                    if self.cabe():
                        self.draw()
                    else:
                        self.xpos = ant 

            if self.left_clicked and not self.ctrl_clicked and self.shift_clicked and self.modoed=='ajuste': # PARALAJE
                if self.direccion == 'y': # ??? cambiar a y
                    print('yanag y', self.yanag)
                    delta = y - self.ym0
                    self.ym0 = y
                    ant = self.yanag
                    if delta>0:
                        self.yanag += 1
                    else:
                        self.yanag -= 1
                    
                    if self.cabe():
                        self.anag0 = make_anag(self.imgi, self.imgd, self.xanag, self.yanag)
                        self.draw()
                    else:
                        self.yanag = ant 

                elif self.direccion == 'x':
                    print('xanag x / p0', self.xanag, self.contoursF.p0)
                    delta = x - self.xm0
                    print(delta, x, self.xm0)
                    self.xm0 = x
                    ant = self.xanag
                    if delta>0:
                        print('inc')
                        self.xanag += 5
                        self.contours.p0 -= 5
                    else:
                        print('dec')
                        self.xanag -= 5
                        self.contours.p0 += 5
                    
                    if self.cabe():
                        # self.anag0 = make_anag(anag, self.xanag, self.yanag)
                        self.anag0 = make_anag(self.imgi, self.imgd, self.xanag, self.yanag)
                        self.draw()
                    else:
                        self.xanag = ant 

                
                # elif self.direccion == 'x':
                #     print('xanag x / xcur', self.xanag, self.poscurx)
                #     delta = x - self.xm0
                #     print(delta, x, self.xm0)
                #     self.xm0 = x
                #     ant = self.xanag
                #     if delta>0:
                #         print('inc')
                #         self.xanag += 5
                #         self.poscurx -= 1
                #     else:
                #         print('dec')
                #         self.xanag -= 5
                #         self.poscurx += 1
                    
                #     if self.cabe():
                #         self.anag0 = make_anag(self.imgi, self.imgd, self.xanag, self.yanag)
                #         self.draw()
                #     else:
                #         self.xanag = ant 


        elif event == cv2.EVENT_LBUTTONUP:
            if self.modoed == 'dib':
                if self.left_clicked and self.xm0 < x and self.ym0 < y: # zoom
                    self.contours.zoom(self.contours.to_map((self.xm0, self.ym0), (self.xm0, self.ym0)),\
                                       self.contours.to_map((x, y), (x, y)))
                    self.draw()

                elif self.ctrl_clicked: # pan
                    ini = self.contours.to_map((self.xm0, self.ym0), (self.xm0, self.ym0))
                    fin = self.contours.to_map((x, y), (x, y))
                    self.contours.pan(ini, fin)
                    self.draw()

            self.left_clicked = False
            self.ctrl_clicked = False

        elif event == cv2.EVENT_RBUTTONDOWN:
            if self.modoed == 'dib':
                self.left_clicked = False
                self.contours.extends()
                self.draw()

        elif event == cv2.EVENT_MOUSEWHEEL:
            if self.direccion == 'y':
                print('rueda y')
            elif self.direccion == 'x':
                print('rueda x')            

    def show(self):
        while True:
            cv2.imshow(self.contours.filename, self.img)
            cv2.setWindowTitle(self.contours.filename, self.contours.filename + ' ' + self.modoed + ' ' + self.parte)
            key = cv2.waitKey(1)
            # if key!=-1:
            #     print(key) 
            if key == 27:
                break
            elif key == 121: # y
                self.direccion = 'y'
            elif key == 120: # x
                self.direccion = 'x'
            elif key == 32: # espacio
                self.direccion = ''
            elif key == 105: # i
                self.dibimagen = not self.dibimagen
                self.draw()
            elif key == 99: # c
                self.dibcurvas = not self.dibcurvas
                self.draw()
            elif key == 102: # f
                if self.parte == '':
                    self.parte = 'i'
                elif self.parte == 'i':
                    self.parte = 'd'
                else:
                    self.parte = ''
                self.draw()
            elif key == 9: # tab
                print(self.modoed)
                if self.modoed == 'dib':
                     self.modoed = 'ajuste'
                else:
                     self.modoed = 'dib'
                cv2.setWindowTitle(self.contours.filename, self.contours.filename + ' ' + self.modoed)
        cv2.destroyAllWindows()


class Contours(object):
    def __init__(self, filename):
        self.filename = filename

        dic = read_dic(self.filename)
        verts = []
        for d in dic['features']:
        	z = d['properties']['id']
        	for x in d['geometry']['coordinates'][0]:
        		y, x, _, _ = conversion.from_latlon(x[1], x[0])
        		verts.append([x, y, z])
        self.vertex0 = np.array(verts)
        self.vertex = np.copy(self.vertex0)

        self.anchoimg = 1000
        self.altoimg = 1000
        self.p0 = 100
        self.poscurx = 7

        if not self.vertex.any():
            return imgl, imgr

        min = np.min(self.vertex, axis=0)
        max = np.max(self.vertex, axis=0)
        self.maxdx = max[0] - min[0]
        self.maxdy = max[1] - min[1]
        self.dz = max[2] - min[2]
        self.minx = min[0]
        self.miny = min[1]
        self.minz = min[2]
        self.maxx = max[0]
        self.maxy = max[1]
        self.maxz = max[2]

    def extends(self):
        self.vertex = self.vertex0

    
    def to_img(self, xyz):
        x, y, z = xyz
        return int((x - self.minx) / self.maxdx * self.anchoimg),\
               int((y - self.miny) / self.maxdy * self.altoimg), \
               self.paralaje(z)
               # int((z - ((self.minz+self.maxz)/2)) / self.dz * self.p0 / 2)     # paralaje


    def to_img_izq(self, xyz):
        self.xposi = 0
        self.yposi = 0 #200
        self.xesci = 1 #1 
        self.yesci = 1 #.5
        x, y, z = xyz
        return int((x - self.minx) / self.maxdx * self.anchoimg * self.xesci) + self.xposi,\
               int((y - self.miny) / self.maxdy * self.altoimg * self.yesci) + self.yposi, \
               self.paralaje(z)
    
    def to_img_der(self, xyz):
        self.xposd = 0
        self.yposd = 0 #400
        self.xescd = 1 
        self.yescd = 1 #.5
        x, y, z = xyz
        return int((x - self.minx) / self.maxdx * self.anchoimg * self.xescd) + self.xposd,\
               int((y - self.miny) / self.maxdy * self.altoimg * self.yescd) + self.yposd, \
               self.paralaje(z)

    def paralaje(self, z):
       return int((z - ((self.minz + self.maxz)/2)) / self.dz * self.p0 / 2) #+ self.poscurx
    
    def to_map(self, xyd, xyi):
        xid, yid = xyd
        xii, yii = xyi
        p = xid - xii
        xi = xid - p/2
        return self.minx + xi * (self.maxx - self.minx) / self.anchoimg, \
               self.miny + yii * (self.maxy - self.miny) / self.altoimg, \
               p / self.p0 * (self.maxz - self.minz) + self.minz

    def draw(self, imgl, imgr, parte):
        self.imgl = imgl
        self.imgr = imgr

        derecho = (255, 255, 141)
        izquierdo = (255, 0, 255)

        izquierdo = (255,0,105)
        derecho = (0,255,0)   

        # anchov, altov = self.vertex.shape
        # z0 = self.vertex[0][2]
        # x0, y0, p = self.to_img(self.vertex[0])
        # for i in range(1, anchov):
        #     z1 = self.vertex[i][2]
        #     x1, y1, p = self.to_img(self.vertex[i])
        #     if z1 == z0:
        #         fun = cv2.line if z1 != 1100 else cv2.arrowedLine
        #         fun(self.imgr, (x0 + p, y0), (x1 + p, y1), izquierdo, thickness=2)
        #         fun(self.imgl, (x0 - p, y0), (x1 - p, y1), derecho, thickness=2)
                
        #     x0, y0, z0 = x1, y1, z1

        anchov, altov = self.vertex.shape
        z0 = self.vertex[0][2]
        xi0, yi0, p = self.to_img_izq(self.vertex[0])
        xd0, yd0, p = self.to_img_der(self.vertex[0])
        # p = paralaje(z0)
        for i in range(1, anchov):
            z1 = self.vertex[i][2]
            xi1, yi1, p = self.to_img_izq(self.vertex[i])
            xd1, yd1, p = self.to_img_der(self.vertex[i])
            # x1, y1, p = self.to_img(self.vertex[i])
            if z1 == z0:
                fun = cv2.line if z1 != 1100 else cv2.arrowedLine
                if parte == 'd' or parte == '':
                    fun(self.imgr, (xd0 + p, yd0), (xd1 + p, yd1), izquierdo, thickness=2)                
                if parte == 'i' or parte == '':
                    fun(self.imgl, (xi0 - p, yi0), (xi1 - p, yi1), derecho, thickness=2)
                
            xi0, yi0, xd0, yd0, z0 = xi1, yi1, xd1, yd1, z1            

        return self.imgl, self.imgr

    def zoom(self, min, max):
        self.xmin, self.ymin, _ = min
        self.xmax, self.ymax, _ = max

        verts = []
        for v in self.vertex0:
            x, y, _ = v
            if x >= self.xmin and x <= self.xmax and y >= self.ymin and y <= self.ymax:
                verts.append(v)
        self.vertex = np.array(verts)

    def pan(self, ini, fin):
        xini, yini, _ = ini
        xfin, yfin, _ = fin
        maxdx = xini - xfin
        maxdy = yini - yfin
        # maxdx = maxdy = 0
        self.xmin += maxdx
        self.xmax += maxdx
        self.ymin += maxdy
        self.ymax += maxdy
        self.zoom((self.xmin, self.ymin, 0), (self.xmax, self.ymax, 0))


contours = Contours('curvasn.geojson')

# img = cv2.imread('2443toda.jpg')
# imgi, imgd = sepanag(img)

imgi = cv2.imread('ValtodaI.jpg')
imgi = cv2.cvtColor(imgi, cv2.COLOR_BGR2GRAY)
imgd = cv2.imread('ValtodaD.jpg')
imgd = cv2.cvtColor(imgd, cv2.COLOR_BGR2GRAY)


img = Image(contours, imgi, imgd)
