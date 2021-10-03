from Render import Render
from utils import color

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

    def load(self, filename, translate, scale, rotate):
        self.render.load(filename, translate, scale, rotate)
        
    def polygon(self, poly):
        self.render.fillPolygon(self.render.drawPolygon(poly))

    def triangle(self, A, B, C, viewport=False):
        self.render.triangle(A, B, C)

    def earth(self, translate=(800, 800, 0), scale=(1,1,1)):
        self.render.loadEarth(translate, scale)

    def texture(self, t):
        self.render.current_texture = t

    def lookAt(self, eye, center, up):
        self.render.lookAt(eye, center, up)

    def draw_arrays(self, arrays="TRIANGLES"):
        self.render.draw_arrays(arrays)