from collections import namedtuple
from Obj import Obj
from utils import *
from Triangle import Triangle
from random import randrange
from LinearAlgebra import *

BLACK = color(0,0,0)
WHITE = color(255,255,255)
RED = color(255,0,0)
GREEN = color(0,255,0)
BLUE = color(0,0,255)

V2 = namedtuple('Vector2', ['x', 'y'])
V3 = namedtuple('Vector3', ['x', 'y', 'z'])

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
        self.zbuffer = [
            [-float('inf') for x in range(self.width)]
            for y in range(self.height)
        ]
        
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
        self.zbuffer = [
            [-float('inf') for x in range(self.width)]
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
                            viewport[int(y*sy + self.viewportY)][int(x*sx + self.viewportX)] = p
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

    def wireframe(self, filename, translate, scale):
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
            for x in range(start, end):
                if toggle_paint:
                    self.framebuffer[y + min(y_list)][x + min(x_list)] = self.current_color
                if(fb_perimeter[y][x]==1):
                    if((not last) and (not (x + min(x_list), y + min(y_list)) in polygon.vertices)):
                        toggle_paint = not toggle_paint
                    last = 1
                else:
                    last = 0

    def zBufferRender(self, v):
        if v.z > self.zbuffer[v.x][v.y]:
            self.zbuffer[v.x][v.y] = v.z
            return True

    def triangle(self, A, B, C, color=None):
        t = Triangle(A, B, C)
        enclosing_max, enclosing_min = t.getEnclosingBox()

        for x in range(enclosing_min.x, enclosing_max.x + 1):
            for y in range(enclosing_min.y, enclosing_max.y + 1):
                w, v, u = t.barycentric(V2(x, y))
                if w < 0 or v < 0 or u < 0:
                    continue

                v = V3(x, y, A.z * w + B.z * v + C.z * u)
                if self.zBufferRender(v):
                    self.framebuffer[y][x] = color or self.current_color

    def transform(self, vertex, translate=(0, 0, 0), scale=(1, 1, 1)):
        return V3(
            round((vertex[0] * scale[0]) + translate[0]),
            round((vertex[1] * scale[1]) + translate[1]),
            round((vertex[2] * scale[2]) + translate[2])
        )

    def load(self, filename, translate, scale, texture=None):
        model = Obj(filename)
        light = V3(0,0,1)

        for face in model.faces:
            vcount = len(face)

            f1 = face[0][0] - 1
            f2 = face[1][0] - 1
            f3 = face[2][0] - 1

            a = self.transform(model.vertices[f1], translate, scale)
            b = self.transform(model.vertices[f2], translate, scale)
            c = self.transform(model.vertices[f3], translate, scale)
            d = None

            if vcount == 3:
                normal = norm(cross(V3(a.x - b.x, a.y - b.y, a.z - b.z), V3(c.x - a.x, c.y - a.y, c.z - a.z)))
            else:
                f4 = face[3][0] - 1   
                d = self.transform(model.vertices[f4], translate, scale)
                normal = norm(cross(V3(a.x - b.x, a.y - b.y, a.z - b.z), V3(b.x - c.x, b.y - c.y, b.z - c.z)))

            intensity = dot(normal, light)
            grey = round(255 * intensity)
            if grey < 0:
                continue

            self.triangle(a, b, c, color=color(grey, grey, grey))
            if d:
                self.triangle(a, c, d, color=color(grey, grey, grey))

    def loadEarth(self, translate, scale):
        model = Obj('earth.obj')
        light = V3(0,0,1)
        centro = V2(round(self.width / 2), round(self.height / 2))
        radio = 400

        for face in model.faces:
            vcount = len(face)

            f1 = face[0][0] - 1
            f2 = face[1][0] - 1
            f3 = face[2][0] - 1

            a = self.transform(model.vertices[f1], translate, scale)
            b = self.transform(model.vertices[f2], translate, scale)
            c = self.transform(model.vertices[f3], translate, scale)
            d = None

            if vcount == 3:
                normal = norm(cross(V3(a.x - b.x, a.y - b.y, a.z - b.z), V3(c.x - a.x, c.y - a.y, c.z - a.z)))
            else:
                f4 = face[3][0] - 1   
                d = self.transform(model.vertices[f4], translate, scale)
                normal = norm(cross(V3(a.x - b.x, a.y - b.y, a.z - b.z), V3(b.x - c.x, b.y - c.y, b.z - c.z)))

            cr, cg, cb = 47, 171, 232
            tierra = 82+randrange(-10,10), 187+randrange(-10,10), 47+randrange(-10,10)
            
            if a.y > 1000 or b.y > 1000 or c.y > 1000:
                if a.x < 1000 or b.x < 1000 or c.x < 1000:
                    cr, cg, cb = tierra
            elif a.y > 950 or b.y > 950 or c.y > 950:
                if (a.x > 550 or b.x > 550 or c.x > 550) and (a.x < 900 or b.x < 900 or c.x < 900) :
                    cr, cg, cb = tierra
            elif a.y > 900 or b.y > 900 or c.y > 900:
                if (a.x > 550 or b.x > 550 or c.x > 550) and (a.x < 650 or b.x < 650 or c.x < 650) :
                    cr, cg, cb = tierra
                if (a.x > 850 or b.x > 850 or c.x > 850) and (a.x < 870 or b.x < 870 or c.x < 870) :
                    cr, cg, cb = tierra
            elif a.y > 850 or b.y > 850 or c.y > 850:
                if (a.x > 580 or b.x > 580 or c.x > 580) and (a.x < 680 or b.x < 680 or c.x < 680) :
                    cr, cg, cb = tierra
                if (a.x > 870 or b.x > 870 or c.x > 870) and (a.x < 900 or b.x < 900 or c.x < 900) :
                    cr, cg, cb = tierra
            elif a.y > 800 or b.y > 800 or c.y > 800:
                if (a.x > 610 or b.x > 610 or c.x > 610) and (a.x < 780 or b.x < 780 or c.x < 780) :
                    cr, cg, cb = tierra
            elif a.y > 750 or b.y > 750 or c.y > 750:
                if (a.x > 680 or b.x > 680 or c.x > 680) and (a.x < 750 or b.x < 750 or c.x < 750) :
                    cr, cg, cb = tierra
            elif a.y > 700 or b.y > 700 or c.y > 700:
                if (a.x > 780 or b.x > 780 or c.x > 780) and (a.x < 900 or b.x < 900 or c.x < 900) :
                    cr, cg, cb = tierra
            elif a.y > 550 or b.y > 550 or c.y > 550:
                if (a.x > 740 or b.x > 740 or c.x > 740) and (a.x < 1000 or b.x < 1000 or c.x < 1000) :
                    cr, cg, cb = tierra
            elif a.y > 400 or b.y > 400 or c.y > 400:
                if (a.x > 830 or b.x > 830 or c.x > 830) and (a.x < 950 or b.x < 950 or c.x < 950) :
                    cr, cg, cb = tierra

            intensity = dot(normal, light)
            cr = round(cr * intensity)
            cg = round(cg * intensity)
            cb = round(cb * intensity)
            if cr+cg+cb <= 0:
                continue
            col = color(cr, cg, cb)

            self.triangle(a, b, c, color=col)
            if d:
                self.triangle(a, c, d, color=col)

    # aqi











                    
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
