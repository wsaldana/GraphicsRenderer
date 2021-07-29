'''
UNIVERSIDAD DEL VALLE DE GUATEMALA
Gráficas por computadoras #10
Walter Saldaña #19897

SR1: POINT
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

            #vph = self.viewportHeight
            
            viewport = [ [self.clear_color for x in range(self.width)] for y in range(self.height) ]

            y_range = self.viewportHeight + self.viewportY
            x_range = self.viewportWidth + self.viewportX
            print(y_range)
            print(self.height)
            
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
                            print(str(x)+" -> "+str(int(x*sx + self.viewportX)))
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
        
    def point(self, x, y, color=None):
        pos_viewport_x = int((x+1)*self.width/2)
        pos_viewport_y = int((y+1)*self.height/2)
        sx =  self.viewportWidth / self.width
        sy =  self.viewportHeight / self.height
        self.framebuffer[int(pos_viewport_y*sy - self.viewportY)][int(pos_viewport_x*sx - self.viewportX)] = color or self.current_color
        
'''
r = Render(1024, 768)
r.point(50,10, GREEN)
r.render()
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

gl = MyGL()
gl.glInit()
gl.glCreateWindow(100,100)
gl.glClearColor(1,1,0)
gl.glClear()
gl.glViewPort(0, 0, 15, 30)
gl.glColor(0,0,1)
gl.glVertex(0, 0)
gl.glFinish('render')