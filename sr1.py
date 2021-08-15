'''
UNIVERSIDAD DEL VALLE DE GUATEMALA
Gráficas por computadoras #10
Walter Saldaña #19897

SR2: LINE
'''

import struct

def char(c):
    # char 1 byte
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    # short 2 bytes
    return struct.pack('=h', w)

def dword(d):
    # long 4 bytes
    return struct.pack('=l', d)

def color(r,g,b):
    return bytes([b,g,r])

BLACK = color(0,0,0)
WHITE = color(255,255,255)
RED = color(255,0,0)
GREEN = color(0,255,0)
BLUE = color(0,0,255)

class Obj(object):
    def __init__(self, filename):
        with open(filename) as f:
            self.lines = f.read().splitlines()
        self.vertices = []
        self.faces = []
        self.read()

    def read(self):
        for line in self.lines:
            if line:
                prefix, value = line.split(' ', 1)

            if prefix == 'v':
                self.vertices.append(
                    list(map(float, value.split(' ')))
                )
            elif prefix == 'f':
                self.faces.append(
                    [list(map(int, face.split('/'))) for face in value.split(' ')]
                )
          
class Polygon(object):
    
    def __init__(self, vertices):
        self.vertices = vertices
        self.normalized_vertices = []
        self.perimeter = []
        
    def normalize(self, n, maximo, minimo):
        return (n-minimo)/(maximo-minimo)
    
    def normalizePolygon(self, vertices=None):
        values = [c for point in vertices for c in point]
        maximo = max(values)
        minimo = min(values)
        normalized = []
        for point in vertices:
            normalized.append((self.normalize(point[0], maximo, minimo), self.normalize(point[1], maximo, minimo)))
        self.normalized_vertices = normalized
        
    def normalizePolygons(self, polygons):
        #joined = [point for polygon in polygons for point in polygon]
        values = [c for point in [point for polygon in polygons for point in polygon] for c in point]
        maximo = max(values)
        minimo = min(values)
        normalized = []
        for polygon in polygons:
            new_polygon = []
            for point in polygon:
                new_polygon.append((self.normalize(point[0], maximo, minimo), self.normalize(point[1], maximo, minimo)))
            normalized.append(new_polygon)
        return normalized

class Render(object):
    def __init__(self):
        self.width = 1024 
        self.height = 768
        self.framebuffer = [
            [BLACK for x in range(self.width)]
            for y in range(self.height)
        ]
        self.viewportX = 0
        self.viewportY = 0
        self.viewportWidth = self.width
        self.viewportHeight = self.height
        self.clear_color = BLACK
        self.current_color = WHITE
        
    def setWidth(self, width):
        self.width = width
        self.viewportWidth = width
        
    def setHeight(self, height):
        self.height = height
        self.viewportHeight = height
        
    def setClearColor(self, color):
        self.clear_color = color
        
    def setCurrentColor(self, color):
        self.current_color = color
        
    def setViewport(self, x, y, width, height):
        self.viewportX = x
        self.viewportY = y
        self.viewportWidth = width
        self.viewportHeight = height
        
    def clear(self):
        self.framebuffer = [
            [self.clear_color for x in range(self.width)]
            for y in range(self.height)
        ]
        
    def write(self, filename):
        with open(filename, 'bw') as f:
            '''File header'''
            f.write(char('B')) #BM
            f.write(char('M'))
            f.write(dword(14 + 40 + 3*(self.width * self.height))) #File size (header+infoheader+data)
            f.write(dword(0)) #0000
            f.write(dword(14 + 40)) # Offset (donde empieza el pixel data)
            
            '''Info header'''
            f.write(dword(40))
            f.write(dword(self.width))
            f.write(dword(self.height))
            f.write(word(1))
            f.write(word(24))
            f.write(dword(0))
            f.write(dword(3*(self.width * self.height)))
            f.write(dword(0))
            f.write(dword(0))
            f.write(dword(0))
            f.write(dword(0))
            
            '''Pixel data / Bitmap (framebuffer)'''
            sx = self.width / self.viewportWidth
            sy = self.height / self.viewportHeight
            
            viewport = [ [self.clear_color for x in range(self.width)] for y in range(self.height) ]

            y_range = self.viewportHeight + self.viewportY
            x_range = self.viewportWidth + self.viewportX
            
            if((y_range <= self.height) and (x_range <= self.width)):
                for y in range(self.viewportY, y_range):
                    for x in range(self.viewportX, x_range):
                        p = self.framebuffer[y][x]
                        if (p != self.clear_color):
                            #viewport[y][x] = p
                            #self.framebuffer[y][x] = self.clear_color
                            viewport[int(y*sy + self.viewportY)][int(x*sx + self.viewportX)] = p
                            #ny = int(y*sy + self.viewportY)
                            #nx = int(x*sx + self.viewportX)
                            #print(str(x)+" -> "+str(int(x*sx + self.viewportX)))
                            #if ((ny >= self.viewportHeight and ny < self.viewportHeight) and ())
                            #viewport[][] = self.framebuffer[y][x]
            else:
                print("El viewport no es válido: se mostrará un viewport con las mismas dimensiones que el window.")
                print("Asegurese que las coordenadas del viewport se encuentren dentro de la window.")
            
            for y in range(self.height):
                for x in range(self.width):
                    f.write(viewport[y][x])
                    
    def render(self, filename):
        self.write(filename+'.bmp')

    #Ingresa una coordenada entre -1,1 y retorna el equivalente a la posicion int en el framebuffer
    def scaleViewportToFB(self, p, s):
        if(s=='x'):
            scale =  self.viewportWidth / self.width
        else:
            scale =  self.viewportHeight / self.height
        return round((p+1)*self.width/2*scale - self.viewportY)
    
    def scaleFBtoViewport(self, p, s):
        if(s=='x'):
            scale =  self.viewportWidth / self.width
        else:
            scale =  self.viewportHeight / self.height
        return 2 * ((p+self.viewportY)/(scale*self.width)) - 1
        
    def point(self, x, y, color=None):
        pos_viewport_x = int((x+1)*self.width/2)
        pos_viewport_y = int((y+1)*self.height/2)
        sx =  self.viewportWidth / self.width
        sy =  self.viewportHeight / self.height
        ny = int(pos_viewport_y*sy - self.viewportY)
        nx = int(pos_viewport_x*sx - self.viewportX)
        if ny<self.height and nx<self.width:
            self.framebuffer[ny][nx] = color or self.current_color

    def line(self, x0, x1, y0, y1, color=None, viewport=True):
        points = []
        if(viewport):
            pos_viewport_x0 = self.scaleViewportToFB(x0, 'x')
            pos_viewport_y0 = self.scaleViewportToFB(y0, 'y')
            pos_viewport_x1 = self.scaleViewportToFB(x1, 'x')
            pos_viewport_y1 = self.scaleViewportToFB(y1, 'y')
        else:
            pos_viewport_x0 = x0
            pos_viewport_y0 = y0
            pos_viewport_x1 = x1
            pos_viewport_y1 = y1

        if((x1 - x0)==0):
            m = 1000000
        else:
            m = (y1 - y0) / (x1 - x0)
        b = pos_viewport_y1 - (m * pos_viewport_x1)

        if(abs(m) <= 1):
            if(x0>x1) :
                pos_viewport_x0, pos_viewport_x1 = pos_viewport_x1, pos_viewport_x0
                pos_viewport_y0, pos_viewport_y1 = pos_viewport_y1, pos_viewport_y0
            for x in range(pos_viewport_x0, pos_viewport_x1+1):
                y = round((m * x) + b)
                self.framebuffer[y][x] = color or self.current_color
                #points.append( (self.scaleFBtoViewport(x, 'x'), self.scaleFBtoViewport(y, 'y')) )
                points.append( (x, y) )
        else:
            if(y0>y1) :
                pos_viewport_x0, pos_viewport_x1 = pos_viewport_x1, pos_viewport_x0
                pos_viewport_y0, pos_viewport_y1 = pos_viewport_y1, pos_viewport_y0
                
            for y in range(pos_viewport_y0, pos_viewport_y1+1):
                x = round((y - b) / m)
                self.framebuffer[y][x] = color or self.current_color
                #points.append( (self.scaleFBtoViewport(x, 'x'), self.scaleFBtoViewport(y, 'y')) )
                points.append( (x, y) )
        return points

    def load(self, filename, translate, scale):
        model = Obj(filename)
        
        for face in model.faces:
            vcount = len(face)
            for j in range(vcount):
                f1 = face[j][0]
                f2 = face[(j + 1) % vcount][0]

                v1 = model.vertices[f1 - 1]
                v2 = model.vertices[f2 - 1]

                x1 = (v1[0] + translate[0]) * scale[0]
                y1 = (v1[1] + translate[1]) * scale[1]
                x2 = (v2[0] + translate[0]) * scale[0]
                y2 = (v2[1] + translate[1]) * scale[1]
                
                self.line(x1, x2, y1, y2)
                
    def drawPolygon(self, polygon, translate=(-0.5,0), scale=(1,1)):
        perimeter = []
        n = len(polygon.vertices)
        for i in range(n):
            x0 = (polygon.vertices[i][0] + translate[0]) * scale[0]
            x1 = (polygon.vertices[(i+1)%n][0] + translate[0]) * scale[0]
            y0 = (polygon.vertices[i][1] + translate[1]) * scale[1]
            y1 = (polygon.vertices[(i+1)%n][1] + translate[1]) * scale[1]
            perimeter += self.line(x0, x1, y0, y1)
        polygon.perimeter = perimeter
        return polygon
    '''
    def fillPolygon(self, polygon):
        x_list = [c[0] for c in polygon.perimeter]
        y_list = [c[1] for c in polygon.perimeter]
        nx = max(x_list)-min(x_list)
        ny = max(y_list)-min(y_list)
        fb_perimeter = [ [1 if (x,y) in polygon.perimeter else 0 for x in range(min(x_list), max(x_list))] for y in range(min(y_list), max(y_list)) ]
        for y in range(len(fb_perimeter)):
            n_vertices = fb_perimeter[y].count(1)
            if n_vertices > 1:
                if(n_vertices % 2 == 0):
                    temp = fb_perimeter[y]
                    acumulador = 0
                    for i in range(int(n_vertices/2)):
                        x0 = temp.index(1)
                        xf = temp[x0+1:].index(1)+x0+1
                        self.line(x0 + min(x_list) + acumulador, xf + min(x_list) + acumulador, y+min(y_list), y+min(y_list), viewport=False)
                        j = 0
                        while temp[0] == 1:
                            temp = temp[xf+1+j:]
                            acumulador += xf+1+j
                else:
                    self.line(fb_perimeter[y].index(1) + min(x_list), len(fb_perimeter[y])-fb_perimeter[y][::-1].index(1) + min(x_list), y+min(y_list), y+min(y_list), viewport=False)
    '''
    
    
    def fillPolygon(self, polygon):
        x_list = [c[0] for c in polygon.perimeter]
        y_list = [c[1] for c in polygon.perimeter]
        nx = max(x_list)-min(x_list)
        ny = max(y_list)-min(y_list)
        fb_perimeter = [ [1 if (x,y) in polygon.perimeter else 0 for x in range(min(x_list), max(x_list))] for y in range(min(y_list), max(y_list)) ]
        for y in range(1,len(fb_perimeter)-1):
            toggle_paint = False
            last = 0
            start = fb_perimeter[y].index(1)
            end = len(fb_perimeter[y])-fb_perimeter[y][::-1].index(1)
            #print((start, end, len(fb_perimeter[y])))
            for x in range(start, end):
                if toggle_paint:
                    self.framebuffer[y + min(y_list)][x + min(x_list)] = self.current_color
                if(fb_perimeter[y][x]==1):
                    if((not last) and (not (x + min(x_list), y + min(y_list)) in polygon.vertices)):
                        toggle_paint = not toggle_paint
                    last = 1
                else:
                    last = 0
    
    
    '''
    def fillPolygon(self, polygon):
        n = 1
        m = 1
        while n>0:
            poly = self.drawPolygon(polygon, translate=(-0.5-(0.001*m),0), scale=(n,n))
            n -= 0.005
            m += 1
    '''
    '''
    def fillPolygon(self, polygon):
        x_list = [c[0] for c in polygon.perimeter]
        y_list = [c[1] for c in polygon.perimeter]
        mx = round((max(x_list)+min(x_list)) / 2)
        my = round((max(y_list)+min(y_list)) / 2)
        for i in range(len(polygon.perimeter)):
            self.line(mx, polygon.perimeter[i][0], my, polygon.perimeter[i][1], viewport=False)
    '''
    '''
    def fillPolygon(self, polygon):
        x_list = [c[0] for c in polygon.perimeter]
        y_list = [c[1] for c in polygon.perimeter]
        mx = (max(x_list)+min(x_list)) / 2
        my = (max(y_list)+min(y_list)) / 2
        n = len(polygon.perimeter)
        for i in range(n):
            for j in range(2):
                if(j==0):
                    print((mx, polygon.perimeter[i][0], my, polygon.perimeter[i][1]))
                    self.line(mx, polygon.perimeter[i][0], my, polygon.perimeter[i][1])
                else:
                    print((mx, (polygon.perimeter[(i+1)%n][0]+polygon.perimeter[i][0])/2, my, (polygon.perimeter[(i+1)%n][1]+polygon.perimeter[i][1])/2))
                    self.line(mx, (polygon.perimeter[(i+1)%n][0]+polygon.perimeter[i][0])/2, my, (polygon.perimeter[(i+1)%n][1]+polygon.perimeter[i][1])/2)
    '''


class MyGL(object):
    def __init__(self):
        self.render = None

    def glInit(self):
        self.render = Render()
        
    def glCreateWindow(self, width, height):
        self.render.setWidth(width)
        self.render.setHeight(height)
        self.render.clear()
        
    def glViewPort(self, x, y, width, height):
        self.render.setViewport(x, y, width, height)
    
    def glClear(self):
        self.render.clear()
        
    def glClearColor(self, r, g, b):
        self.render.setClearColor(color(r*255,g*255,b*255))
        
    def glVertex(self, x, y):
        self.render.point(x, y)
    
    def glColor(self, r, g, b):
        self.render.setCurrentColor(color(r*255,g*255,b*255))
        
    def glFinish(self, filename):
        self.render.render(filename)

    def glLine(self, x0, y0, x1, y1):
        self.render.line(x0, x1, y0, y1)

    def load(self, filename, translate, scale):
        self.render.load(filename, translate, scale)
        
    def polygon(self, poly):
        self.render.fillPolygon(self.render.drawPolygon(poly))

gl = MyGL()
gl.glInit()
gl.glCreateWindow(1600, 1600)
gl.glClearColor(0,0,0)
gl.glClear()
gl.glViewPort(0, 0, 1600, 1600)
gl.glColor(0,1,0)
#gl.glVertex(-0.5, -0.5)
#gl.glColor(0,0,0)
#gl.glLine(0.5, 0.5, -0.5, 0)
#gl.glColor(1,0,0)
#gl.glLine(-0.9, 0.4, -0.1, 0.6)
gl.load("Pokemon.obj", (0, -1), (0.8, 0.8))

'''
poly = Polygon([(1,2)])
polys = poly.normalizePolygons((
    ((165, 380), (185, 360), (180, 330), (207, 345), (233, 330), (230, 360), (250, 380), (220, 385), (205, 410), (193, 383)),
    ((321, 335), (288, 286), (339, 251) ,(374, 302)),
    ((377, 249), (411, 197), (436, 249)),
    ((413, 177), (448, 159), (502, 88), (553, 53), (535, 36), (676, 37), (660, 52), (750, 145), (761, 179), (672, 192) ,(659, 214), (615, 214), (632, 230), (580, 230), (597, 215), (552, 214), (517, 144), (466, 180)),
    ((682, 175), (708, 120), (735, 148), (739, 170))
))

poly1 = Polygon(polys[0])
poly2 = Polygon(polys[1])
poly3 = Polygon(polys[2])
poly4 = Polygon(polys[3])
poly5 = Polygon(polys[4])

gl.polygon(poly1)
gl.polygon(poly2)
gl.polygon(poly3)
gl.polygon(poly4)
gl.glColor(0,0,0)
gl.polygon(poly5)
'''

gl.glFinish('render')