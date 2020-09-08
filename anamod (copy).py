import numpy as np
import conversion
import cv2

def read_dic(filename):
    with open(filename, 'r') as f:
        dic = eval(f.read())    
    return dic

def show(window, img):
    cv2.imshow(window, img)
    while True:
        key = cv2.waitKey(1)
        print(key) 
        if key == 27:
            break
    cv2.destroyAllWindows()

def make_anag(img, x, y):
    (rows,cols, _) = img.shape
    M = np.float32([[1,0,x], [0,1,y]])
    imgl = cv2.warpAffine(img[:, :, 1], M, (cols,rows)) # izquierda
    imgr = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    derecho = (255, 255, 141)
    izquierdo = (255, 0, 255)

    # El derecho es el magenta (red + blue) -> magenta
    anag = np.zeros(img.shape, dtype=np.uint8)
    anag[:, :, 2] = (imgr * (141. /255)).astype(np.uint8) + (imgl * .5).astype(np.uint8)         # R
    anag[:, :, 1] = imgr        # G
    anag[:, :, 0] = (imgr * .5).astype(np.uint8) + (imgl * .5).astype(np.uint8)
    return anag

def fit(img, ancho, alto, x, y):
    (rows,cols, _) = img.shape

    # if rows>cols:
    #     ancho = int(ancho * cols / rows)
    # else:
    #     alto = int(alto * rows /cols)

    img = cv2.resize(img, (ancho, alto), interpolation=cv2.INTER_LINEAR)
    # print('fit shape', img.shape)
    return make_anag(img, x, y)

def insert(grande, peq, x, y):
    grande[y: y + peq.shape[0], x: x + peq.shape[1]] = peq
    return grande 


class Image(object):
    def __init__(self, contours, anag, xanag, yanag):
        self.contours = contours
        self.dibcurvas = True
        self.dibimagen = True
        self.direccion = 'x'
        self.modoed = 'dib'

        self.xsize = 700
        self.ysize = 620
        self.xpos = 300
        self.ypos = 250

        self.xanag = xanag
        self.yanag = yanag
        self.anag0 = make_anag(anag, self.xanag, self.yanag)

        cv2.namedWindow(contours.filename)
        cv2.setMouseCallback(contours.filename, self.onmouse)

    def dibujaImagen(self, ancho, alto):
        # propx = self.dx / ancho
        # propy = self.dy / alto
        # if propx > propy:
        #     self.ancho = ancho
        #     self.alto = int(alto * propy / propx)
        # else: 
        #     self.alto = alto
        #     self.ancho = int(ancho * propx / propy)

        self.ancho, self.alto = ancho, alto      

        self.imgr = np.zeros([self.ancho, self.alto, 3], dtype=np.uint8)
        self.imgl = np.zeros([self.ancho, self.alto, 3], dtype=np.uint8)
        self.img  = np.zeros([self.ancho, self.alto, 3], dtype=np.uint8)

        # imagen
        if self.dibimagen:
            # imgx =  cv2.resize(self.anag0, (700, 620), interpolation=cv2.INTER_LINEAR) # tamaño
            # self.anag = insert(self.img, imgx, 300, 250) # posicion

            imgx =  cv2.resize(self.anag0, (self.xsize, self.ysize), interpolation=cv2.INTER_LINEAR) # tamaño
            self.anag = insert(self.img, imgx, self.xpos, self.ypos) # posicion
            
            # self.anag = fit(self.anag0, self.ancho, self.alto, -48, 6)
            self.imgl[:, :, 2] = self.anag[:, :, 2]        # R -> R
            self.imgr[:, :, 1] = self.anag[:, :, 1]        # G -> G
            self.imgl[:, :, 0] = self.anag[:, :, 0]        # B -> B
        else:
            self.imgr[:, :, :] = 255
            self.imgl[:, :, :] = 255
    
    def to_img(self, xyz):
        x, y, z = xyz
        return int((x - self.minx) / self.dx * self.ancho),\
               int((y - self.miny) / self.dy * self.alto), \
               self.paralaje(z)
               # int((z - ((self.minz+self.maxz)/2)) / self.dz * self.p0 / 2)     # paralaje

    def paralaje(self, z):
       return int((z - ((self.minz+self.maxz)/2)) / self.dz * self.p0 / 2)     # paralaje
               # int((z - self.minz) / self.dz * self.p0 / 2)     # paralaje
               # aqui se puede jugar con la distancia entre las imagenes

    def to_map(self, xyd, xyi):
        xid, yid = xyd
        xii, yii = xyi
        p = xid - xii
        xi = xid - p/2
        return self.minx + xi * (self.maxx - self.minx) / self.ancho, \
               self.miny + yii * (self.maxy - self.miny) / self.alto, \
               p / self.p0 * (self.maxz - self.minz) + self.minz

    def draw_contours(self):
        vertex = self.contours.vertex
        min = np.min(vertex, axis=0)
        max = np.max(vertex, axis=0)
        self.dx = max[0] - min[0]
        self.dy = max[1] - min[1]
        self.dz = max[2] - min[2]
        self.minx = min[0]
        self.miny = min[1]
        self.minz = min[2]
        self.maxx = max[0]
        self.maxy = max[1]
        self.maxz = max[2]

        self.p0 = 30    # paralaje de base
        magenta = (int(255*.7),0,255)
        verde = (int(255*.037),255,int(255*.221))

        derecho = (255, 255, 141)
        izquierdo = (255, 0, 255)

        # izquierdo = (255,0,105)
        # derecho = (0,255,0)        

        self.dibujaImagen(1000, 1000)      # maximos para calcular el ancho y alto de la foto
        
        if self.dibcurvas:
            anchov, altov = vertex.shape
            z0 = vertex[0][2]
            x0, y0, p = self.to_img(vertex[0])
            for i in range(1, anchov):
                z1 = vertex[i][2]
                x1, y1, p = self.to_img(vertex[i])
                if z1 == z0:
                    fun = cv2.line if z1 != 1100 else cv2.arrowedLine
                    fun(self.imgr, (x0 + p, y0), (x1 + p, y1), izquierdo, thickness=2)
                    fun(self.imgl, (x0 - p, y0), (x1 - p, y1), derecho, thickness=2)
                    
                x0, y0, z0 = x1, y1, z1

        self.img[:, :, 0] = self.imgl[:, :, 0]
        self.img[:, :, 1] = self.imgr[:, :, 1]
        self.img[:, :, 2] = self.imgl[:, :, 2]

        self.clicked = False
        self.clicked_ctrl = False
        self.xm0, self.ym0 = 0,0
        self.show()

    def onmouse(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.clicked = True
            self.xm0, self.ym0 = x, y

            if flags == cv2.EVENT_FLAG_CTRLKEY + cv2.EVENT_FLAG_LBUTTON:
                self.clicked = False
                self.clicked_ctrl = True
        
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.clicked:
                if self.direccion == 'y':
                    print('mueve y')
                elif self.direccion == 'x':
                    print('mueve x')

        elif event == cv2.EVENT_LBUTTONUP:
            if self.modoed == 'dib':
                if self.clicked and self.xm0 < x and self.ym0 < y: # zoom
                    self.clicked = False
                    self.contours.zoom(self.to_map((self.xm0, self.ym0), (self.xm0, self.ym0)),\
                                       self.to_map((x, y), (x, y)))
                    self.draw_contours()

                elif self.clicked_ctrl: # pan
                    self.clicked_ctrl = False
                    ini = self.to_map((self.xm0, self.ym0), (self.xm0, self.ym0))
                    fin = self.to_map((x, y), (x, y))
                    self.contours.pan(ini, fin)
                    self.draw_contours()

        elif event == cv2.EVENT_RBUTTONDOWN:
            if self.modoed == 'dib':
                self.clicked = False
                self.contours.extends()
                self.draw_contours()

        elif event == cv2.EVENT_MOUSEWHEEL:
            if self.direccion == 'y':
                print('rueda y')
            elif self.direccion == 'x':
                print('rueda x')            

    def show(self):
        cv2.imshow(self.contours.filename, self.img)
        cv2.setWindowTitle(self.contours.filename, self.contours.filename + ' ' + self.modoed)
        while True:
            key = cv2.waitKey(1)
            if key!=-1:
                print(key) 
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
                self.draw_contours()
            elif key == 99: # c
                self.dibcurvas = not self.dibcurvas
                self.draw_contours()
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

    def extends(self):
        self.vertex = self.vertex0

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
        dx = xini - xfin
        dy = yini - yfin
        # dx = dy = 0
        self.xmin += dx
        self.xmax += dx
        self.ymin += dy
        self.ymax += dy
        self.zoom((self.xmin, self.ymin, 0), (self.xmax, self.ymax, 0))


anag = cv2.imread('2443toda.jpg')
contours = Contours('curvasn.geojson')
img = Image(contours, anag, -2000, 30)
img.draw_contours()
cv2.destroyAllWindows()