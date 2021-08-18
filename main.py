'''
UNIVERSIDAD DEL VALLE DE GUATEMALA
Gráficas por computadoras #10
Walter Saldaña #19897
'''

from MyGL import MyGL
from Polygon import Polygon

gl = MyGL()
gl.glInit()
gl.glCreateWindow(1600, 1600)
gl.glClearColor(0,0,0)
gl.glClear()
gl.glViewPort(0, 0, 1600, 1600)
gl.glColor(0,1,0)
#gl.glVertex(-0.5, -0.5)
#gl.glLine(-0.9, 0.4, -0.1, 0.6)
gl.load("Pokemon.obj", (800, 200, 0), (700, 700, -700))
#gl.triangle((10, 70), (50, 160), (70, 80))
#gl.triangle((-0.5, 0), (0, -0.5), (0.5, 0.5))

gl.glFinish('render')