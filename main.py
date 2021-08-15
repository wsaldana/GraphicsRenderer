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
gl.load("Pokemon.obj", (0, -1), (0.8, 0.8))

gl.glFinish('render')